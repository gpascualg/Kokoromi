from appium import webdriver
from ..pipeline import Pipeline

class AppiumTest:
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
