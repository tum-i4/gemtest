from gemtest.metamorphic_test_case import UninitializedValue
from gemtest.report.execution_report import GeneralMTCExecutionReport


def test_not_generated_source_outputs():
    report = GeneralMTCExecutionReport()
    report.source_outputs = [UninitializedValue for _ in range(5)]
    assert all(v == "(not generated)" for v in report.source_outputs)


def test_not_generated_followup_inputs():
    report = GeneralMTCExecutionReport()
    report.followup_inputs = [UninitializedValue for _ in range(5)]
    assert all(v == "(not generated)" for v in report.followup_inputs)


def test_not_generated_followup_outputs():
    report = GeneralMTCExecutionReport()
    report.followup_outputs = [UninitializedValue for _ in range(5)]
    assert all(v == "(not generated)" for v in report.followup_outputs)


def test_not_generated_empty_followup_inputs():
    report = GeneralMTCExecutionReport()
    report.followup_inputs = []
    assert "(not generated)" == report.followup_inputs[0]
    assert all(v == "(not generated)" for v in report.followup_inputs)


def test_not_generated_empty_followup_outputs():
    report = GeneralMTCExecutionReport()
    report.source_outputs = [UninitializedValue for _ in range(5)]
    report.followup_outputs = []
    assert "(not generated)" == report.followup_outputs[0]
    assert all(v == "(not generated)" for v in report.followup_outputs)
