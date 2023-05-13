import os
from appium import webdriver

from .python_test import PythonTest
from ..pipeline import Pipeline

class AppiumTest(PythonTest):
    driver : webdriver.Remote = None

    @staticmethod
    def caps():
        config = Pipeline.instance().current_stage.config
        application_id = config.get('application_id')

        if application_id:
            return {
                "app": application_id
            }

        return {}

    @classmethod
    def on_failed(cls, report, request) -> None:
        PythonTest.on_failed(report, request)
        # TODO(gpascualg): Take screenshot with Appium
        #cls.driver.save_screenshot(os.path.join('outputs', request.node.name))
