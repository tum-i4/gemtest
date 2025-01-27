import datetime

from gemtest.metamorphic_test_case import UninitializedValue


class GeneralMTCExecutionReport:
    """
    An execution report contains all information to create a string report or html report.
    It only stores the name of functions.
    """

    def __init__(self):
        self.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.mtc_name: str = ""
        self.mr_name: str = ""
        self.sut_name: str = ""
        self._source_inputs = []
        self._source_outputs = []
        self._followup_inputs = []
        self._followup_outputs = []
        self.transformation_name: str = ""
        self.relation_name: str = ""
        self.test_result: str = ""
        self.relation_result: bool = False
        self.parameters = {}
        self.stdout: str = ""
        self.stderr: str = ""
        self.duration: int = 0

    def populate(self, report):
        names = report.nodeid.replace("]", "")
        names = names.split("[")[1]
        names = names.split(", ")
        self.sut_name = names[0].split("=")[1]
        self.mr_name = names[1].split(".")[1]
        self.mtc_name = names[2].split("=")[1]
        self.test_result = report.outcome
        self.stdout = report.capstdout
        self.stderr = report.capstderr
        self.duration = report.duration

    @property
    def source_inputs(self):
        return self._source_inputs

    @source_inputs.setter
    def source_inputs(self, value):
        self._source_inputs = value

    @property
    def source_outputs(self):
        return self._source_outputs

    @source_outputs.setter
    def source_outputs(self, value):
        self._source_outputs = [
            "(not generated)" if v is UninitializedValue else v for v in value
        ]

    @property
    def followup_inputs(self):
        return self._followup_inputs

    @followup_inputs.setter
    def followup_inputs(self, value):
        if value:
            self._followup_inputs = [
                "(not generated)" if v is UninitializedValue else v for v in value
            ]
        else:
            self._followup_inputs = ["(not generated)"]

    @property
    def followup_outputs(self):
        return self._followup_outputs

    @followup_outputs.setter
    def followup_outputs(self, value):
        if value:
            self._followup_outputs = [
                "(not generated)" if v is UninitializedValue else v for v in value
            ]
        else:
            self._followup_outputs = ["(not generated)"] * len(self.source_outputs)
