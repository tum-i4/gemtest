from gemtest.report.execution_report import GeneralMTCExecutionReport


class GeneralDataExporter:

    def __init__(self, data_exporter, report: GeneralMTCExecutionReport):
        self.data_exporter = data_exporter
        self.report = report

    def execute(self):
        self.data_exporter(report=self.report)
