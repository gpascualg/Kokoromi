from lib.utils.python_test import PythonTest

class TestSimple(PythonTest):
    def test_eq(self):
        assert __file__ == 2
