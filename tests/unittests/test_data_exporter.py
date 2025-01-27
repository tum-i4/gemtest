from gemtest import GeneralMTCExecutionReport
from gemtest.report.data_exporter import GeneralDataExporter

mr_name = "test_mr"


def export_data(report: GeneralMTCExecutionReport):
    assert mr_name == report.mr_name


def test_data_exporter():
    report1 = GeneralMTCExecutionReport()
    report1.mr_name = mr_name

    exporter = GeneralDataExporter(export_data, report1)
    exporter.execute()
