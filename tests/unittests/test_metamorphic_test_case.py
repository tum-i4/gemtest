import pytest

from gemtest.metamorphic_test_case import MetamorphicTestCase


def test_source_input_getter_setter():
    metamorphic_test_case = MetamorphicTestCase()
    metamorphic_test_case.source_inputs = 1

    assert metamorphic_test_case.source_inputs == [1]
    assert metamorphic_test_case.source_input == 1

    metamorphic_test_case.source_inputs = 2
    assert metamorphic_test_case.source_inputs == [1, 2]

    with pytest.raises(ValueError):
        test = metamorphic_test_case.source_input

    metamorphic_test_case.source_inputs = tuple([3, 4])
    assert metamorphic_test_case.source_inputs == [1, 2, 3, 4]

    metamorphic_test_case.source_inputs = [5, 6]
    assert metamorphic_test_case.source_inputs == [5, 6]


def test_source_output_getter_setter():
    metamorphic_test_case = MetamorphicTestCase()
    metamorphic_test_case.source_outputs = 1

    assert metamorphic_test_case.source_outputs == [1]
    assert metamorphic_test_case.source_output == 1

    metamorphic_test_case.source_outputs = 2

    assert metamorphic_test_case.source_outputs == [1, 2]
    with pytest.raises(ValueError):
        test = metamorphic_test_case.source_output

    metamorphic_test_case.source_outputs = tuple([3, 4])
    assert metamorphic_test_case.source_outputs == [1, 2, 3, 4]

    metamorphic_test_case.source_outputs = [5, 6]
    assert metamorphic_test_case.source_outputs == [5, 6]


def test_followup_input_getter_setter():
    metamorphic_test_case = MetamorphicTestCase()
    metamorphic_test_case.followup_inputs = 1

    assert metamorphic_test_case.followup_inputs == [1]
    assert metamorphic_test_case.followup_input == 1

    metamorphic_test_case.followup_inputs = 2

    assert metamorphic_test_case.followup_inputs == [1, 2]
    with pytest.raises(ValueError):
        test = metamorphic_test_case.followup_input

    metamorphic_test_case.followup_inputs = tuple([3, 4])
    assert metamorphic_test_case.followup_inputs == [1, 2, 3, 4]

    metamorphic_test_case.followup_inputs = [5, 6]
    assert metamorphic_test_case.followup_inputs == [5, 6]


def test_followup_output_getter_setter():
    metamorphic_test_case = MetamorphicTestCase()
    metamorphic_test_case.followup_outputs = 1

    assert metamorphic_test_case.followup_outputs == [1]
    assert metamorphic_test_case.followup_output == 1

    metamorphic_test_case.followup_outputs = 2

    assert metamorphic_test_case.followup_outputs == [1, 2]
    with pytest.raises(ValueError):
        test = metamorphic_test_case.followup_output

    metamorphic_test_case.followup_outputs = tuple([3, 4])
    assert metamorphic_test_case.followup_outputs == [1, 2, 3, 4]

    metamorphic_test_case.followup_outputs = [5, 6]
    assert metamorphic_test_case.followup_outputs == [5, 6]


def test_relation_result_getter_setter():
    metamorphic_test_case = MetamorphicTestCase()
    metamorphic_test_case.relation_result = True

    assert metamorphic_test_case.relation_result
    with pytest.raises(ValueError):
        metamorphic_test_case.relation_result = "this should fail"


def test_parameters_getter_setter():
    metamorphic_test_case = MetamorphicTestCase()
    metamorphic_test_case.parameters = {'a': 1}

    assert metamorphic_test_case.parameters == {'a': 1}
    with pytest.raises(ValueError):
        metamorphic_test_case.parameters = "this should fail"

def test_report_getter_setter():
    metamorphic_test_case = MetamorphicTestCase()
    metamorphic_test_case.report = "Initial Report"

    assert metamorphic_test_case.report == "Initial Report"

    metamorphic_test_case.report = "Updated report"
    assert metamorphic_test_case.report == "Updated report"


def test_error_getter_setter():
    metamorphic_test_case = MetamorphicTestCase()
    metamorphic_test_case.error = "Initial error"

    assert metamorphic_test_case.error == "Initial error"

    metamorphic_test_case.error = "Updated error"
    assert metamorphic_test_case.error == "Updated error"
