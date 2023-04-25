from __future__ import annotations
from .. import plugin
from .. stages import report 

class Plugin(plugin.Plugin):
    def __init__(self, pipe, stage):
        super().__init__('Report', pipe, stage, tuple())

    def call(self, stage: Stage, inputs: dict, outputs: tuple[dict, bool]) -> tuple[dict, bool]:
        report.Stage.add_results(stage, outputs)
        return outputs
