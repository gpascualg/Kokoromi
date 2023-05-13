from appium import webdriver
import pytest

from ..pipeline import Pipeline
from ..utils.phase_report_key import phase_report_key

@pytest.fixture(autouse=True, scope='class')
def _setup_appium_resources(request):
    config = Pipeline.instance().stage_config('appium')
    server : str = config.get('server')
    caps : dict = config.get('caps')

    assert server, "Provide a server for the appium plugin"
    assert caps, "Provide default caps for the appium plugin"

    if hasattr(request.cls, 'caps'):
        caps.update(request.cls.caps())

    yield
    return

    request.cls.driver = webdriver.Remote(server, caps)
    assert request.cls.driver, "No driver could be built"
    yield
    request.cls.driver.close()

@pytest.fixture(autouse=True)
def _callbacks_appium(request):
    yield

    assert phase_report_key in request.node.stash, request.node.report_call
    report = request.node.stash[phase_report_key]
    if report['call'].failed:
        request.cls.on_failed(report, request)
