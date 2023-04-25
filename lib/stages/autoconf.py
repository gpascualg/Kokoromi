from __future__ import annotations
from .. import stage
from ..plugins import autoconf_plugin

class Stage(stage.Stage):
    def __init__(self, pipe, config):
        super().__init__('AutoConf', pipe, config,
                         ('application', 'config', 'autoconf-config'),
                         ('application', 'config'))

    def pipeline_ready(self):
        plugin = autoconf_plugin.Plugin(self.pipe, self)

        # Find previous Obfuscator and Appium nodes
        current_index = self.pipe.current_stages.index(self)
        stages = list(reversed(self.pipe.current_stages[:current_index]))
        prev_obfuscator = next(stage for stage in stages if stage.name == 'Obfuscator')
        prev_appium = next(stage for stage in stages if stage.name == 'Appium')

        # Add plugin to each of them and init.
        prev_obfuscator.add_plugin(plugin)
        prev_appium.add_plugin(plugin)
        plugin.initialize_from(prev_obfuscator, prev_appium)

        return True

    def call(self, inputs):
        return {
                'application': inputs['application'], 
                'config': inputs['config'] + '.merged'
                }, True
