import pytest
import math

from gemtest.metamorphic_error import SUTExecutionError
from gemtest.metamorphic_relation import MetamorphicRelation
from gemtest.metamorphic_test_case import MetamorphicTestCase
from gemtest.testing_strategy import TestingStrategy

DATA = range(100)


def dummy_transformation(source_input):
    followup_input = source_input
    return followup_input


def dummy_relation(source_output, followup_output):
    return source_output == followup_output


def dummy_system(system_input):
    return system_input


def test_create_parameter_permutations_sample():
    sut_parameters = {"x": [1, 2], "y": [3, 4]}
    mr = MetamorphicRelation(mr_id="mr1",
                             data=DATA,
                             testing_strategy=TestingStrategy.SAMPLE,
                             number_of_test_cases=1,
                             number_of_sources=1)
    mr.sut_parameters = sut_parameters
    assert mr.create_parameter_permutations() == [
        {'x': 1, 'y': 3},
        {'x': 1, 'y': 4},
        {'x': 2, 'y': 3},
        {'x': 2, 'y': 4}
    ]


def test_create_parameter_permutations_exhaustive():
    sut_parameters = {"x": [1, 2], "y": [3, 4]}
    mr = MetamorphicRelation(mr_id="mr1",
                             data=DATA,
                             testing_strategy=TestingStrategy.EXHAUSTIVE,
                             number_of_test_cases=1,
                             number_of_sources=1)
    mr.sut_parameters = sut_parameters
    assert mr.create_parameter_permutations() == [
        {'x': 1, 'y': 3},
        {'x': 1, 'y': 4},
        {'x': 2, 'y': 3},
        {'x': 2, 'y': 4}
    ]


def test_create_parameter_permutations_no_params_sample():
    sut_parameters = {}
    mr = MetamorphicRelation(mr_id="mr1",
                             data=DATA,
                             testing_strategy=TestingStrategy.SAMPLE,
                             number_of_test_cases=1,
                             number_of_sources=1)
    mr.sut_parameters = sut_parameters
    assert mr.create_parameter_permutations() == [{}]


def test_create_parameter_permutations_no_params_exhaustive():
    sut_parameters = {}
    mr = MetamorphicRelation(mr_id="mr1",
                             data=DATA,
                             testing_strategy=TestingStrategy.EXHAUSTIVE,
                             number_of_test_cases=1,
                             number_of_sources=1)
    mr.sut_parameters = sut_parameters
    assert mr.create_parameter_permutations() == [{}]


def test_generate_test_cases_valid_input():
    mr = MetamorphicRelation(mr_id="mr1", data=DATA,
                             testing_strategy=TestingStrategy.SAMPLE,
                             number_of_test_cases=2,
                             number_of_sources=2)
    mr.generate_test_cases()
    assert len(mr.mtc_templates) == 2


def test_generate_test_cases_invalid_number_of_test_cases():
    mr = MetamorphicRelation(mr_id="mr1", data=DATA,
                             testing_strategy=TestingStrategy.SAMPLE,
                             number_of_test_cases=-1,
                             number_of_sources=1)
    with pytest.raises(ValueError):
        mr.generate_test_cases()


def test_generate_test_cases_invalid_number_of_sources():
    mr = MetamorphicRelation(mr_id="mr1", data=DATA,
                             testing_strategy=TestingStrategy.SAMPLE,
                             number_of_test_cases=2,
                             number_of_sources=0)
    with pytest.raises(ValueError):
        mr.generate_test_cases()


def test_generate_test_cases_empty_data():
    mr = MetamorphicRelation(mr_id="mr1", data=[],
                             testing_strategy=TestingStrategy.SAMPLE,
                             number_of_test_cases=2,
                             number_of_sources=1)
    with pytest.raises(ValueError):
        mr.generate_test_cases()


def test_generate_test_cases_number_of_test_cases_larger_than_data():
    mr = MetamorphicRelation(mr_id="mr1", data=DATA,
                             testing_strategy=TestingStrategy.SAMPLE,
                             number_of_test_cases=1000,
                             number_of_sources=1)
    with pytest.raises(ValueError):
        mr.generate_test_cases()


def test_generate_test_cases_number_of_sources_larger_than_data():
    mr = MetamorphicRelation(mr_id="mr1", data=DATA,
                             testing_strategy=TestingStrategy.SAMPLE,
                             number_of_test_cases=1,
                             number_of_sources=1000)
    with pytest.raises(ValueError):
        mr.generate_test_cases()


def test_no_transformation_on_metamorphic_relation():
    mr = MetamorphicRelation(mr_id="mr1", data=DATA,
                             testing_strategy=TestingStrategy.SAMPLE,
                             number_of_test_cases=1,
                             number_of_sources=1)

    with pytest.raises(ValueError):
        test_case = MetamorphicTestCase()
        mr.apply_transformation(test_case)


def test_transformation_multiple_sources_on_metamorphic_relation():
    mr = MetamorphicRelation(mr_id="mr1", data=DATA,
                             testing_strategy=TestingStrategy.SAMPLE,
                             number_of_test_cases=1,
                             number_of_sources=2)

    mr.transform = dummy_transformation

    with pytest.raises(ValueError):
        test_case = MetamorphicTestCase()
        mr.apply_transformation(test_case)


def test_transformation_parameters_on_metamorphic_relation():
    mr = MetamorphicRelation(mr_id="mr1", data=DATA,
                             testing_strategy=TestingStrategy.SAMPLE,
                             number_of_test_cases=1,
                             number_of_sources=2)

    mr.transform = dummy_transformation
    mr.sut_parameters = {"x": [1, 2], "y": [3, 4]}

    with pytest.raises(ValueError):
        test_case = MetamorphicTestCase()
        test_case.source_inputs = 1
        mr.apply_transformation(test_case)


def test_no_relation_on_metamorphic_relation():
    mr = MetamorphicRelation(mr_id="mr1", data=DATA,
                             testing_strategy=TestingStrategy.SAMPLE,
                             number_of_test_cases=1,
                             number_of_sources=1)

    with pytest.raises(ValueError):
        test_case = MetamorphicTestCase()
        mr.apply_relation(test_case)


def test_relation_multiple_sources_on_metamorphic_relation():
    mr = MetamorphicRelation(mr_id="mr1", data=DATA,
                             testing_strategy=TestingStrategy.SAMPLE,
                             number_of_test_cases=1,
                             number_of_sources=2)

    mr.relation = dummy_relation

    with pytest.raises(ValueError):
        test_case = MetamorphicTestCase()
        mr.apply_relation(test_case)


def test_relation_multiple_followups_on_metamorphic_relation():
    mr = MetamorphicRelation(mr_id="mr1", data=DATA,
                             testing_strategy=TestingStrategy.SAMPLE,
                             number_of_test_cases=1,
                             number_of_sources=1)

    mr.relation = dummy_relation

    with pytest.raises(ValueError):
        test_case = MetamorphicTestCase()
        test_case.followup_outputs = [1, 2]
        mr.apply_relation(test_case)


def test_relation_parameters_on_metamorphic_relation():
    mr = MetamorphicRelation(mr_id="mr1", data=DATA,
                             testing_strategy=TestingStrategy.SAMPLE,
                             number_of_test_cases=1,
                             number_of_sources=2)

    mr.relation = dummy_relation
    mr.sut_parameters = {"x": [1, 2], "y": [3, 4]}

    with pytest.raises(ValueError):
        test_case = MetamorphicTestCase()
        test_case.source_inputs = 1
        mr.apply_relation(test_case)


def test_multiple_sut_on_metamorphic_relation():
    mr = MetamorphicRelation(mr_id="mr1", data=DATA,
                             testing_strategy=TestingStrategy.SAMPLE,
                             number_of_test_cases=1,
                             number_of_sources=1)

    mr.system_under_test = dummy_system

    with pytest.raises(ValueError):
        mr.system_under_test = dummy_system


def test_multiple_transforms_on_metamorphic_relation():
    mr = MetamorphicRelation(mr_id="mr1", data=DATA,
                             testing_strategy=TestingStrategy.SAMPLE,
                             number_of_test_cases=1,
                             number_of_sources=1)

    mr.transform = dummy_transformation

    with pytest.raises(ValueError):
        mr.transform = dummy_transformation


def test_multiple_general_transforms_on_metamorphic_relation():
    mr = MetamorphicRelation(mr_id="mr1", data=DATA,
                             testing_strategy=TestingStrategy.SAMPLE,
                             number_of_test_cases=1,
                             number_of_sources=1)

    mr.general_transform = dummy_transformation

    with pytest.raises(ValueError):
        mr.general_transform = dummy_transformation


def test_multiple_relations_on_metamorphic_relation():
    mr = MetamorphicRelation(mr_id="mr1", data=DATA,
                             testing_strategy=TestingStrategy.SAMPLE,
                             number_of_test_cases=1,
                             number_of_sources=1)

    mr.relation = dummy_relation

    with pytest.raises(ValueError):
        mr.relation = dummy_relation


def test_multiple_general_relation_on_metamorphic_relation():
    mr = MetamorphicRelation(mr_id="mr1", data=DATA,
                             testing_strategy=TestingStrategy.SAMPLE,
                             number_of_test_cases=1,
                             number_of_sources=1)

    mr.general_relation = dummy_relation

    with pytest.raises(ValueError):
        mr.general_relation = dummy_relation


def test_source_sut_exception():
    def sut_function(input):
        raise Exception

    mr = MetamorphicRelation(mr_id="mr1",
                             data=DATA,
                             testing_strategy=TestingStrategy.SAMPLE,
                             number_of_test_cases=1,
                             number_of_sources=1)

    mr.system_under_test = sut_function
    mtc = MetamorphicTestCase()
    mtc.source_inputs = 1
    mtc.followup_inputs = 1
    sut_id = sut_function.__name__

    # Test source outputs
    # SystemExit caused by the SUTExecutionError will be caught here
    with pytest.raises(SystemExit) as excinfo:
        mr.create_source_outputs(mtc, sut_id)
    assert isinstance(mtc.error, SUTExecutionError)
    # Confirm that SystemExit was raised
    assert isinstance(excinfo.value, SystemExit)

    mtc.error = None

    # Test followup outputs
    with pytest.raises(SystemExit) as excinfo:
        mr.create_followup_outputs(mtc, sut_id)
    assert isinstance(mtc.error, SUTExecutionError)
    assert isinstance(excinfo.value, SystemExit)

def test_relation_multiple_followups():
    mr = MetamorphicRelation(mr_id="mr1",
                             data=DATA,
                             testing_strategy=TestingStrategy.SAMPLE,
                             number_of_test_cases=1,
                             number_of_sources=1)

    mr.relation = dummy_relation
    mtc = MetamorphicTestCase()
    mtc.source_outputs = 1
    mtc.followup_outputs = [1, 2]

    with pytest.raises(ValueError):
        mr.apply_relation(mtc)


def test_relation_parameters():
    mr = MetamorphicRelation(mr_id="mr1",
                             data=DATA,
                             testing_strategy=TestingStrategy.SAMPLE,
                             number_of_test_cases=1,
                             number_of_sources=1,
                             sut_parameters={"a": 1})

    mr.relation = dummy_relation
    mtc = MetamorphicTestCase()
    mtc.source_outputs = 1
    mtc.followup_outputs = 1

    with pytest.raises(ValueError):
        mr.apply_relation(mtc)


def test_transform_setter():
    mr = MetamorphicRelation(mr_id="mr1",
                             data=DATA,
                             testing_strategy=TestingStrategy.SAMPLE,
                             number_of_test_cases=1,
                             number_of_sources=1,
                             sut_parameters={"a": 1})

    mr.general_transform = dummy_transformation

    with pytest.raises(ValueError):
        mr.transform = dummy_transformation


def test_general_transform_setter():
    mr = MetamorphicRelation(mr_id="mr1",
                             data=DATA,
                             testing_strategy=TestingStrategy.SAMPLE,
                             number_of_test_cases=1,
                             number_of_sources=1,
                             sut_parameters={"a": 1})

    mr.transform = dummy_transformation

    with pytest.raises(ValueError):
        mr.general_transform = dummy_transformation


def test_relation_setter():
    mr = MetamorphicRelation(mr_id="mr1",
                             data=DATA,
                             testing_strategy=TestingStrategy.SAMPLE,
                             number_of_test_cases=1,
                             number_of_sources=1,
                             sut_parameters={"a": 1})

    mr.general_relation = dummy_transformation

    with pytest.raises(ValueError):
        mr.relation = dummy_transformation


def test_general_relation_setter():
    mr = MetamorphicRelation(mr_id="mr1",
                             data=DATA,
                             testing_strategy=TestingStrategy.SAMPLE,
                             number_of_test_cases=1,
                             number_of_sources=1,
                             sut_parameters={"a": 1})

    mr.relation = dummy_transformation

    with pytest.raises(ValueError):
        mr.general_relation = dummy_transformation

def test_calculate_possible_sources():
    mr = MetamorphicRelation(mr_id="mr1",
                             data=DATA,
                             testing_strategy=TestingStrategy.SAMPLE,
                             number_of_test_cases=1,
                             number_of_sources=3)  # r = 3
    expected_value = math.factorial(len(DATA)) / (math.factorial(3) * math.factorial(len(DATA) - 3))
    assert mr._calculate_possible_sources() == expected_value

def test_calculate_possible_sources_with_one_source():
    mr = MetamorphicRelation(mr_id="mr1",
                             data=DATA,
                             testing_strategy=TestingStrategy.SAMPLE,
                             number_of_test_cases=1,
                             number_of_sources=1)  # r = 1
    assert mr._calculate_possible_sources() == len(DATA)  # Should return n

def test_calculate_possible_sources_with_zero_sources():
    mr = MetamorphicRelation(mr_id="mr1",
                             data=DATA,
                             testing_strategy=TestingStrategy.SAMPLE,
                             number_of_test_cases=1,
                             number_of_sources=0)  # r = 0
    assert mr._calculate_possible_sources() == 1  # C(n, 0) = 1

def test_calculate_possible_sources_with_more_sources_than_elements():
    mr = MetamorphicRelation(mr_id="mr1",
                             data=DATA,
                             testing_strategy=TestingStrategy.SAMPLE,
                             number_of_test_cases=1,
                             number_of_sources=len(DATA) + 1)  # r > n
    # Value Error appears with r > n in math.factorial(n - r). Negative Factorial not defined. 
    with pytest.raises(ValueError):
        mr._calculate_possible_sources()
