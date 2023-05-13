import os
import pytest

from ..pipeline import Pipeline

BASE_PATH = os.path.realpath(os.path.join(
    os.path.dirname(__file__), '..', '..'))

class TestsTracker:
    def __init__(self):
        self.tests = set()

    def pytest_runtest_logreport(self, report):
        self.tests.add(report)


def run_pytest(test, *plugins):
    tracker = TestsTracker()
    result = pytest.main([
        os.path.join(BASE_PATH, test),
        '--html', 
        f'reports/{Pipeline.instance().current_test_name}.html', 
        '--self-contained-html'
        ], plugins=[tracker, 'lib.plugins.pytest_fixtures', *plugins])

    return result, tracker.tests
