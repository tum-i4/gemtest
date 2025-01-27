import math
import pytest
import gemtest as gmt
from tests.end2end.conftest import test_results, get_test_file_name

mr_1 = gmt.create_metamorphic_relation(name='mr_1',
                                       data=range(100),
                                       testing_strategy=gmt.TestingStrategy.SAMPLE,
                                       number_of_sources=1,
                                       number_of_test_cases=10)

mr_2 = gmt.create_metamorphic_relation(name='mr_2',
                                       data=range(100),
                                       testing_strategy=gmt.TestingStrategy.SAMPLE,
                                       number_of_sources=1,
                                       number_of_test_cases=10)

mr_3 = gmt.create_metamorphic_relation(name='mr_3',
                                       data=range(100),
                                       testing_strategy=gmt.TestingStrategy.SAMPLE,
                                       number_of_sources=1,
                                       number_of_test_cases=10)

mr_4 = gmt.create_metamorphic_relation(name='mr_4',
                                       data=range(100),
                                       testing_strategy=gmt.TestingStrategy.SAMPLE,
                                       number_of_sources=1,
                                       number_of_test_cases=10)

mr_5 = gmt.create_metamorphic_relation(name='mr_5',
                                       data=range(100),
                                       testing_strategy=gmt.TestingStrategy.SAMPLE,
                                       number_of_sources=1,
                                       number_of_test_cases=10)

mr_6 = gmt.create_metamorphic_relation(name='mr_6',
                                       data=range(100),
                                       testing_strategy=gmt.TestingStrategy.SAMPLE,
                                       number_of_sources=1,
                                       number_of_test_cases=10)

parameters = {"random_t": [1, 2, 3]}

mr_7 = gmt.create_metamorphic_relation(name='mr_7',
                                       data=range(100),
                                       testing_strategy=gmt.TestingStrategy.EXHAUSTIVE,
                                       number_of_sources=1,
                                       parameters=parameters,
                                       number_of_test_cases=10)

parameters_duplicate = {"n": [1], "c": [0]}

mr_8 = gmt.create_metamorphic_relation(name='mr_8',
                                       data=range(100),
                                       testing_strategy=gmt.TestingStrategy.EXHAUSTIVE,
                                       number_of_sources=1,
                                       parameters=parameters_duplicate,
                                       number_of_test_cases=10)


# General transformation with randomized and fixed parameters in different orders
@gmt.general_transformation(mr_1)
@gmt.randomized('n', gmt.RandInt(1, 10))
@gmt.fixed('c', 0)
def dummy_general_transformation_order_1(mtc: gmt.MetamorphicTestCase, n: int, c: int):
    followup = mtc.source_input + 2 * n * math.pi + c
    return followup

@gmt.general_transformation(mr_2)
@gmt.fixed('c', 0)
@gmt.randomized('n', gmt.RandInt(1, 10))
def dummy_general_transformation_order_2(mtc: gmt.MetamorphicTestCase, n: int, c: int):
    followup = mtc.source_input + 2 * n * math.pi + c
    return followup


@gmt.general_transformation(mr_3)
@gmt.fixed('c', 0)
def dummy_general_transformation_fixed_only(mtc: gmt.MetamorphicTestCase, c: int):
    followup = mtc.source_input + c
    return followup


# General transformation with only randomized parameters
@gmt.general_transformation(mr_4)
@gmt.randomized('n', gmt.RandInt(1, 10))
def dummy_general_transformation_random(mtc: gmt.MetamorphicTestCase, n: int):
    followup = mtc.source_input + 2 * n * math.pi
    return followup

@gmt.general_transformation(mr_5)
@gmt.randomized('n', gmt.RandInt(1, 10))
@gmt.randomized('t', gmt.RandInt(1, 10))
@gmt.fixed('c', 0)
def dummy_general_transformation_2_args_random(mtc: gmt.MetamorphicTestCase, n: int, c: int, t: int):
    followup = mtc.source_input + 2 * (n * t) * math.pi + c
    return followup

@gmt.general_transformation(mr_6)
@gmt.randomized('n', gmt.RandInt(1, 10))
@gmt.fixed('c', 0)
@gmt.randomized('t', gmt.RandInt(1, 10))
@gmt.fixed('d', 0)
@gmt.fixed('e', 0)
def dummy_general_transformation_2_args_random(mtc: gmt.MetamorphicTestCase, n: int, c: int, t: int, d: int, e: int):
    followup = mtc.source_input + 2 * (n * t) * math.pi + c + d + e 
    return followup

@gmt.general_transformation(mr_7)
@gmt.randomized('n', gmt.RandInt(1, 10))
@gmt.fixed('c', 0)
def dummy_general_transformation_2_args_random(mtc: gmt.MetamorphicTestCase, n: int, c: int):
    t = mtc.parameters['random_t']
    followup = mtc.source_input + 2 * (n * t) * math.pi + c
    return followup

@gmt.general_transformation(mr_8)
@gmt.randomized('n', gmt.RandInt(1, 10))
@gmt.fixed('c', 0)
def dummy_general_transformation_duplicate_parameters(mtc: gmt.MetamorphicTestCase, n: int, c: int):
    followup = mtc.source_input + 2 * n * math.pi + c
    return followup

# General relation reusing transformation parameters
@gmt.general_relation(mr_1)
def dummy_general_relation_reuse_params_order_1(mtc: gmt.MetamorphicTestCase):
    n = mtc.parameters['n']
    c = mtc.parameters['c']
    result = mtc.source_output + n + c == pytest.approx(mtc.followup_output + n + c)
    return result


@gmt.general_relation(mr_2)
def dummy_general_relation_reuse_params_order_2(mtc: gmt.MetamorphicTestCase):
    n = mtc.parameters['n']
    c = mtc.parameters['c']
    result = mtc.source_output + n + c == pytest.approx(mtc.followup_output + n + c)
    return result

@gmt.general_relation(mr_3)
def dummy_general_relation_reuse_params_fixed_only(mtc: gmt.MetamorphicTestCase):
    c = mtc.parameters['c']
    result = mtc.source_output + c == pytest.approx(mtc.followup_output + c)
    return result


@gmt.general_relation(mr_4)
def dummy_general_relation_random(mtc: gmt.MetamorphicTestCase):
    n = mtc.parameters['n']
    result = mtc.source_output + n == pytest.approx(mtc.followup_output + n)
    return result

@gmt.general_relation(mr_5)
def dummy_general_relation_2_args_random(mtc: gmt.MetamorphicTestCase):
    n = mtc.parameters['n']
    c = mtc.parameters['c']
    t = mtc.parameters['t']
    result = mtc.source_output + n*t + c == pytest.approx(mtc.followup_output + n*t + c)
    return result

@gmt.general_relation(mr_6)
def dummy_general_relation_2_args_random(mtc: gmt.MetamorphicTestCase):
    n = mtc.parameters['n']
    c = mtc.parameters['c']
    t = mtc.parameters['t']
    d = mtc.parameters['d']
    e = mtc.parameters['e']
    result = mtc.source_output + n*t + c + d + e == pytest.approx(mtc.followup_output + n*t + c + d + e)
    return result

@gmt.general_relation(mr_7)
def dummy_general_relation_2_args_random(mtc: gmt.MetamorphicTestCase):
    n = mtc.parameters['n']
    c = mtc.parameters['c']
    t = mtc.parameters['random_t']
    result = mtc.source_output + n*t + c == pytest.approx(mtc.followup_output + n*t + c)
    return result

@gmt.general_relation(mr_8)
def dummy_general_relation_duplicate_params(mtc: gmt.MetamorphicTestCase):
    n = mtc.parameters['n']
    c = mtc.parameters['c']
    result = mtc.source_output + n + c == pytest.approx(mtc.followup_output + n + c)
    return result

@pytest.mark.xfail()
@gmt.system_under_test(mr_1, mr_2, mr_3, mr_4, mr_5, mr_6, mr_7)
def test_dummy_sut(input: float) -> float:
    return math.sin(input)


@pytest.mark.xfail()
@gmt.system_under_test(mr_8)
def test_dummy_sut_systemexit(input: float) -> float:
    """
     Tests Relation with expected Systemexit due to duplicate parameters.
    """
    with pytest.raises(SystemExit):
        return math.sin(input)

def test_framework_tests():
    KEY = get_test_file_name()
    assert test_results[KEY]['number_of_passed_tests'] == 360
    assert test_results[KEY]['number_of_failed_tests'] == 100
