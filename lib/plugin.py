from __future__ import annotations
from typing import Sequence, Callable

from enum import Enum


class Plugin:
    def __init__(self, name: str, pipe: Pipeline, stage: Stage, outputs: Sequence[str]):
        self.name = name
        self.pipe = pipe
        self.stage = stage
        self.base_outputs = outputs
        self.hooks : dict[str, Callable]

    def __call__(self, stage: Stage, inputs: dict, outputs: tuple[dict, bool]) -> tuple[dict, bool]:
        return self.call(stage, inputs, outputs)

    def call(self, stage: Stage, inputs: dict, outputs: tuple[dict, bool]) -> tuple[dict, bool]:
        return outputs

    @property
    def outputs(self):
        return self.base_outputs
