import pytest

from gemtest.report.execution_report import GeneralMTCExecutionReport
from gemtest.report.string_generator import StringReportGenerator


@pytest.fixture
def sample_execution_report_single():
    report = GeneralMTCExecutionReport()
    report.mtc_name = "Your MTC Name"
    report.mr_name = "Your MR Name"
    report.sut_name = "Your SUT Name"
    report._source_inputs = ["source_input_1"]
    report._source_outputs = ["source_output_1"]
    report._followup_inputs = ["followup_input_1"]
    report._followup_outputs = ["followup_output_1"]
    report.transformation_name = "Your Transformation Name"
    report.relation_name = "Your Relation Name"
    report.relation_result = True
    report.parameters = {"this_is_param1": "this_is_value1"}

    return report


def test_string_generator_single(sample_execution_report_single):
    generator = StringReportGenerator(sample_execution_report_single)
    report_string = generator.generate()
    expected_report_string = \
        ("""                       parameters: {'this_is_param1': 'this_is_value1'}
---------------------------------------------------------------------------------------------
|                                                                                           |
|   source_input_1               ------ Your SUT Name ----->              source_output_1   |
|   |                                                                                   |   |
|   | Your Transformation Name                                                          |   |
|   |                                                                                   |   |
|   followup_input_1             ------ Your SUT Name ----->            followup_output_1   |
|                                                                                           |
---------------------------------------------------------------------------------------------
    |------------------------->    Your Relation Name: True    <-------------------------|""")
    assert report_string == expected_report_string


def test_string_generator_multiple(sample_execution_report_single):
    sample_execution_report_single.source_inputs.append("source_input_2")
    sample_execution_report_single.followup_inputs.append("followup_input_2")
    sample_execution_report_single.source_outputs.append("source_output_2")
    sample_execution_report_single.followup_outputs.append("followup_output_2")
    sample_execution_report_single.parameters["this_is_a_very_long_param2"] = \
        "this_is_a_very_long_value2"

    generator = StringReportGenerator(sample_execution_report_single)
    report_string = generator.generate()
    expected_report_string = \
        ("""parameters: {'this_is_param1': 'this_is_value1', 'this_is_a_very_long_param2': 'this_is_a_ver...
---------------------------------------------------------------------------------------------
|                                                                                           |
|   source_input_1               ------ Your SUT Name ----->              source_output_1   |
|   source_input_2               ------ Your SUT Name ----->              source_output_2   |
|   |                                                                                   |   |
|   | Your Transformation Name                                                          |   |
|   |                                                                                   |   |
|   followup_input_1             ------ Your SUT Name ----->            followup_output_1   |
|   followup_input_2             ------ Your SUT Name ----->            followup_output_2   |
|                                                                                           |
---------------------------------------------------------------------------------------------
    |------------------------->    Your Relation Name: True    <-------------------------|""")
    assert report_string == expected_report_string
