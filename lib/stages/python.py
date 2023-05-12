from __future__ import annotations
import os
import pytest

from .. import stage

class Plugin:
    def __init__(self):
        self.passed_tests = set()

    def pytest_runtest_logreport(self, report):
        self.passed_tests.add(report)

BASE_PATH = os.path.realpath(os.path.join(
    os.path.dirname(__file__), '..', '..'))

class Stage(stage.Stage):
    def __init__(self, pipe, config):
        super().__init__('Python', pipe, config, ('test',), ('results',))

    def call(self, inputs):
        test = os.path.join(BASE_PATH, inputs['test'])
        plugin = Plugin()
        pytest.main([test], plugins=[plugin])
        return {'results': plugin.passed_tests}, True
