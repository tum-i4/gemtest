import atexit
from typing import Dict

import pytest

from .logger import logger
from .report.data_exporter import GeneralDataExporter
from .report.report_handler import ReportHandler
from .report.string_generator import StringReportGenerator

CONFIG: Dict = {}
report_handler: ReportHandler
printed_hints = set()


def get_conftest_config():
    return CONFIG


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "metamorphic_relation(mtc, module): mark test as metamorphic_relation"
    )


def find_metamorphic_relation_mark(item):
    for mark in item.iter_markers(name='metamorphic_relation'):
        return mark


def pytest_addoption(parser):
    parser.addoption(
        "--string-report",
        action="store_true",
        default=False,
        help="Enable custom string report feature",
    )
    parser.addoption(
        "--html-report",
        action="store_true",
        default=False,
        help="Enable custom html report feature",
    )
    parser.addoption(
        "--batch_size",
        default=None,
        help="Set batch size",
    )
    parser.addoption(
        "--sut_filepath",
        default=None,
        help="Set SUT filepath",
    )
    parser.addoption(
        "--sut_class",
        default=None,
        help="Set SUT classname",
    )
    parser.addoption(
        "--export-data",
        action="store_true",
        default=False,
        help="Enable data export feature",
    )
    parser.addoption(
        "--disable-logger",
        action="store_true",
        default=False,
        help="set logging level"
    )


@pytest.fixture(scope='session')
def config(request):
    string_report = request.config.getoption('--string-report')
    return {
        'string_report': string_report
    }


def update_config_sut_dynamic(session):
    sut_filepath = session.config.getoption('--sut_filepath')
    sut_class = session.config.getoption('--sut_class')
    sut_dynamic = (sut_filepath is not None and sut_class is not None)
    CONFIG['sut_filepath'] = sut_filepath
    CONFIG['sut_class'] = sut_class
    CONFIG['is_sut_dynamic_active'] = sut_dynamic


def pytest_sessionstart(session):
    """
    The wrapper that gets called before all tests are executed.
    """
    global CONFIG
    CONFIG = {
        'string_report': session.config.getoption('--string-report'),
        'html_report': session.config.getoption('--html-report'),
        'batch_size': session.config.getoption('--batch_size'),
        'export_data': session.config.getoption('--export-data'),
    }
    if CONFIG['html_report']:
        global report_handler
        report_handler = ReportHandler(max_size=100)
    update_config_sut_dynamic(session)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.TestReport, call: pytest.CallInfo):
    """
    The wrapper that gets called during the test execution for each test case. If a test is
    marked as metamorphic_relation, then the wrapper will generate the reports (string /
    html) and export the data depending on which options are set.
    """
    pytest_html = item.config.pluginmanager.getplugin("html")
    mr_mark: pytest.Mark = find_metamorphic_relation_mark(item)

    if not (pytest_html and mr_mark):
        yield
        return

    outcome = yield
    report = outcome.get_result()

    if call.excinfo is not None and isinstance(call.excinfo.value, SystemExit):
        raise call.excinfo.value

    if report.when == "call":

        mtc = item.callspec.params['mtc']
        if mtc.report:
            mtc.report.populate(report)

        data_exporter = mr_mark.kwargs.get("data_exporter", None)

        if data_exporter:
            if CONFIG["export_data"]:
                export_test_data(data_exporter, mtc.report)
            else:
                printed_hints.add("export_data")
        if CONFIG['string_report']:
            generate_string_report(mtc)
        if CONFIG['html_report']:
            generate_html_report(mtc, mr_mark)


def export_test_data(data_exporter, report):
    exporter = GeneralDataExporter(data_exporter, report)
    exporter.execute()


def generate_string_report(mtc):
    logger.info("\n%s\n", StringReportGenerator(mtc.report).generate())
    if mtc.error:
        logger.error(mtc.error)


def generate_html_report(mtc, mr_mark):
    input_visualizer = mr_mark.kwargs.get("visualize_input", None)
    output_visualizer = mr_mark.kwargs.get("visualize_output", None)
    report_handler.add_report(mtc, input_visualizer, output_visualizer)  # noqa


def print_hint_message():
    hints = []
    if "export_data" in printed_hints:
        hints.append(
            "A data exporter was detected but intentionally not run. "
            "To also run the exporter, use the command line flag --export-data"
        )
    if "html_report" in printed_hints:
        hints.append(
            "This test was run with the command line flag --html-report."
            "\n\033[1m\033[93mTo visualize test results in the webapp, "
            "install the webapp by running:"
            "\n\033[94mpip install gemtest-webapp"
            "\n\033[1m\033[93mLaunch the webapp by running:"
            "\n\033[94mgemtest-webapp --results-dir "
            "<path-to-gemtest-results-folder>\033[0m\033[0m"
        )

    for hint in hints:
        print(hint)


def pytest_sessionfinish(session, exitstatus):  # noqa
    """
    The wrapper that gets called after all tests are executed.
    """
    if CONFIG['html_report']:
        report_handler.save()  # noqa
        report_handler.close()  # noqa
        # When the test suite run without errors, add the hint
        if exitstatus in (0, 1):
            # Executes the print_hint_message at termination.
            printed_hints.add("html_report")

    atexit.register(print_hint_message)
