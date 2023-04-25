from .. import stage


class Stage(stage.Stage):
    def __init__(self, pipe, config):
        super().__init__('Obfuscator', pipe, config, ('application', 'config'), ('application',))

    def call(self, inputs):
        return {'application': inputs['application'] + '.obfuscated'}, True


