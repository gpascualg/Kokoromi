from appium import webdriver
import pytest

from ..pipeline import Pipeline

@pytest.fixture(autouse=True, scope='class')
def _setup_appium_resources(request):
    config = Pipeline.instance().stage_config('appium')
    server : str = config.get('server')
    caps : dict = config.get('caps')

    assert server, "Provide a server for the appium plugin"
    assert caps, "Provide default caps for the appium plugin"

    if hasattr(request.cls, 'caps'):
        caps.update(request.cls.caps())

    request.cls.driver = webdriver.Remote(server, caps)
    assert request.cls.driver, "No driver could be built"
    yield
    request.cls.driver.close()
