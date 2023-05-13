from __future__ import annotations
import pytest

from ..utils.phase_report_key import phase_report_key

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item):
    outcome = yield

    # Make sure the report is accessible from the fixtures.
    report = outcome.get_result()
    item.stash.setdefault(phase_report_key, {})[report.when] = report

    # Obtain the test and perform callbacks.
    test : Optional[PythonTest] = getattr(item.obj, '__self__', None)
    test_method = getattr(test, f'on_test_{report.when}', None)
    if test_method:
        test_method(report)

    # Add more information to the HTML report only if this is the call reportself.
    if report.when != "call":
        return

    # Obtain the existing extras.
    pytest_html = item.config.pluginmanager.getplugin("html")
    extra = getattr(report, "extra", [])

    # Add any screenshot that has been taken
    html = '<div style="max-width: 100%">'
    for screenshot in test.screenshots:
        html += f'<img src="{screenshot}" style="max-width:250px;" />'
    html += '</div>'
    extra.append(pytest_html.extras.html(html))

    # Save the newly added information.
    report.extra = extra
