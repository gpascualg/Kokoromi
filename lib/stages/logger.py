from __future__ import annotations
import logging

from .. import stage
from ..pipeline import Pipeline
from ..plugins import report_plugin

class Stage(stage.Stage):
    all_outputs = {}

    def __init__(self, pipe, config):
        super().__init__('Report', pipe, config, tuple(), tuple())

    def verify(self, outputs):
        assert False, "Do not add an explicit Report stage"

    def call(self, inputs):
        assert False, "Do not add an explicit Report stage"

    @classmethod
    def start(cls):
        config = Pipeline.instance().stage_config(Stage)
        level = config.get('level', 'info')

        def map_level():
            if level.lower() == 'debug':
                return logging.DEBUG
            if level.lower() == 'info':
                return logging.INFO
            if level.lower() == 'warning':
                return logging.WARNING
            if level.lower() == 'error':
                return logging.ERROR
            if level.lower() == 'critical':
                return logging.CRITICAL
            assert False, 'Unexpected logging level'

        logging.basicConfig()
        logging.getLogger().setLevel(map_level())
