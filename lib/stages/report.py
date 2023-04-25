from __future__ import annotations
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
        print(f'Building HTML report for pipe {Pipeline.instance()}')
        print(Stage.all_outputs)
