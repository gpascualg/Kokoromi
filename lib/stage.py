from __future__ import annotations
from typing import Sequence
import itertools as it
import copy
import inspect
import logging
import os

from .plugin import Plugin

class Stage:
    def __init__(self, name: str, pipe: Pipeline, config: dict, requirements: Sequence[str], base_outputs: Sequence[str]):
        self.name = name
        self.pipe = pipe
        self.config = config
        self.requirements = requirements
        self.base_outputs = base_outputs
        self.has_run = False
        self.plugins : List[Plugin] = []

    @classmethod
    def class_name(cls):
        cls_name = inspect.getfile(cls)
        cls_name = os.path.basename(cls_name)[:-3]
        return cls_name

    @property
    def allows_failure(self) -> bool:
        return self.config.get('allow-failure', False)

    @property
    def always_runs(self) -> bool:
        return self.config.get('always-runs', False)
    
    @property
    def expects_failure(self) -> bool:
        return self.config.get('expects-failure', False)

    @property
    def outputs(self):
        return it.chain(self.base_outputs, *(x.outputs for x in self.plugins))

    def was_successful(self, result: bool) -> bool:
        if self.allows_failure:
            return True

        # Expected failures invert the result
        if self.expects_failure:
            return not result

        return result

    def add_plugin(self, plugin):
        self.plugins.append(plugin)

    def must_run(self) -> bool:
        return self.always_runs and not self.has_run

    def pipeline_ready(self):
        return True

    def verify(self, inputs: Sequence[str]):
        for req in self.requirements:
            assert req in self.config or req in inputs, f'Missing input {req} for {self.name}'
        return True

    def __call__(self, inputs: dict) -> tuple[dict, bool]:
        self.has_run = True

        # Produce inputs by preferring incoming inputs.
        merged = copy.copy(self.config)
        merged.update(inputs)

        # Setup, if any.
        self.setup()

        # Call the stage and associated plugins.
        logging.debug(' > > Calling stage `%s(%s)`', self.name, merged)
        outputs = self.call(merged)
        for plugin in self.plugins:
            outputs = plugin(self, merged, outputs)

        next_inputs, result = outputs
        logging.debug(' > > > Success: %s', result)
        logging.debug(' > > > Output: %s', next_inputs)

        # Do any teardown.
        self.teardown()

        return outputs

    def call(self, inputs: dict) -> tuple[dict, bool]:
        raise NotImplementedError(f'Stage {self.name} not implemented')

    def setup(self):
        pass

    def teardown(self):
        pass

    @classmethod
    def start(cls):
        pass

    @classmethod
    def on_pipeline_created(cls):
        pass

    @classmethod
    def finish(cls):
        pass
