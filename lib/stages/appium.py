from __future__ import annotations
import os
import pytest

from .. import stage
from ..utils.pytest_helper import run_pytest


class Stage(stage.Stage):
    def __init__(self, pipe, config):
        super().__init__('Appium', pipe, config, ('test', 'application',), ('results',))

    def call(self, inputs):
        result, tests = run_pytest(inputs['test'], 'lib.plugins.appium_fixtures')
        return {'results': tests}, result
