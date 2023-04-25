from __future__ import annotations
from .. import stage


class Stage(stage.Stage):
    def __init__(self, pipe, config):
        super().__init__('Appium', pipe, config, ('application',), ('results',))

    def call(self, inputs):
        return {'results': True}, True

