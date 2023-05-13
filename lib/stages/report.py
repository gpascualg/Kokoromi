from __future__ import annotations
import logging
import subprocess

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
    def on_pipeline_created(cls):
        test_name = Pipeline.instance().current_test_name
        config = Pipeline.instance().stage_config(cls)
        if test_name in config.get('skip', []):
            return

        plugin = report_plugin.Plugin(Pipeline.instance(), None)

        for stg in Pipeline.instance().current_stages:
            stg.add_plugin(plugin)

        return True

    @classmethod
    def add_results(cls, stg: Stage, outputs: tuple[dict, bool]):
        try:
            results = Stage.all_outputs[stg.pipe.current_test_name]
        except KeyError:
            Stage.all_outputs[stg.pipe.current_test_name] = []
            results = Stage.all_outputs[stg.pipe.current_test_name]

        results.append((stg, outputs))

    @classmethod
    def finish(cls):
        # Merge all html reports into a single one.
        logging.debug(f'Building HTML report for pipe {Pipeline.instance()}')
        subprocess.check_call(['pytest_html_merger', '-i', 'reports', '-o', 'report.html'])
