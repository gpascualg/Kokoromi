import random
from lib.utils.appium_test import AppiumTest

class TestSomeApp(AppiumTest):
    def test_sth(self):
        assert random.randrange(0, 2) == 1
