from __future__ import annotations
from .. import plugin

class Plugin(plugin.Plugin):
    def __init__(self, pipe, stage):
        super().__init__('AutoConfPlugin', pipe, stage, ('application', 'config', 'autoconf-config'))
        self.autoconf_config = None

    def initialize_from(self, obfuscator: Stage, appium: Stage):
        self.application = obfuscator.config['application']
        self.config = obfuscator.config['config']

    def call(self, stage: Stage, inputs: dict, outputs: tuple[dict, bool]) -> tuple[dict, bool]:
        # If it is the obfuscator step, we just return the same outputs as the
        # obfuscator would have.
        if stage.name == 'Obfuscator':
            # TODO: Fetch the actual autoconf configuration via Appium
            return outputs

        # Otherwise, after the Appium step we return the original application
        # with its config, and the autoconf obtained config.
        return {'application': self.application,
                'config': self.config,
                'autoconf-config': self.autoconf_config}, True
