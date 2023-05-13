
class PythonTest:
    def setup_class(self) -> None:
        self.screenshots : List[str] = []

    def teardown_class(self):
        pass

    def on_test_setup(self, report) -> None:
        pass

    def on_test_call(self, report) -> None:
        pass

    def on_test_teardown(self, report) -> None:
        pass

    @classmethod
    def on_failed(cls, report, request) -> None:
        pass
