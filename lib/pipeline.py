from __future__ import annotations
import yaml
import logging

class Pipeline:
    INSTANCE : Optional[Pipeline] = None

    def __init__(self, config_path: str, stages: dict):
        self.config_path = config_path
        self.current_stages : list[Stage] = []
        self.current_test_name : Optional[str] = None
        self.all_pipes : list[tuple[str, list[Stage]]] = []
        self.stages = stages
        self.config : dict = {}
        Pipeline.INSTANCE = self

    @staticmethod
    def instance() -> Pipeline:
        return Pipeline.INSTANCE

    def parse_stage(self, stage_info):
        name = next(iter(stage_info.keys()))
        config = stage_info[name] or {}
        stage = self.stages[name](self, config)
        return stage

    def stage_config(self, stage: Union[Stage, str]):
        class_name = stage if isinstance(stage, str) else stage.class_name()
        return self.config.get(class_name, {})

    def execute(self):
        with open(self.config_path, 'r') as fp:
            config = yaml.safe_load(fp)

        assert config.get('version') == 2, 'Unsupported version'

        # Load global config, if any, and verify that each item is a valid Stage name.
        self.config = config.get('config', {})
        assert all(key in self.stages for key in self.config), "Invalid config provided"

        # Start every stage at class level to prepare setup if any is needed.
        for stage in self.stages.values():
            stage.start()

        for test_name, test_stages in config['tests'].items():
            # Constuct the list of stages
            logging.info("Executing test `%s`", test_name)
            self.current_test_name = test_name
            self.current_stages = [self.parse_stage(x) for x in test_stages]
            self.all_pipes.append((test_name, self.current_stages))
            logging.info(" > %s", " > ".join(x.name for x in self.current_stages))

            # Let stages perform any initialization.
            assert all(x.pipeline_ready() for x in self.current_stages)

            # Verify that all stages have the required information
            logging.info(" > Performing stages verification")
            assert all(y.verify(x.outputs) for x, y in zip(self.current_stages, self.current_stages[1:])), 'All stages should verify'

            # Run class level hooks.
            for stage in self.stages.values():
                stage.on_pipeline_created()

            # Actually call them
            logging.info(" > Running pipeline")
            inputs = {}
            for stage in self.current_stages:
                self.current_stage = stage
                inputs, result = stage(inputs)
                if not stage.was_successful(result):
                    break

            # There are stages that might need to run always, even if the previous step resulted in a failure.
            for stage in self.current_stages:
                if not stage.always_runs:
                    continue

                # This stages run with empty inputs and returned results are ignored
                stage({})

        # Teardown every stage at class level type after all tests have run
        # This allows to aggregate all data if needed by the stage type
        for stage in self.stages.values():
            stage.finish()
