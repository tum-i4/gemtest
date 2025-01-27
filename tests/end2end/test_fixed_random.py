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


@gmt.transformation(mr_1)
@gmt.randomized('n', gmt.RandInt(1, 10))
@gmt.fixed('c', 0)
def dummy_transformation(source_input: int, n: int, c: int):
    return source_input + 2 * n * math.pi + c


@gmt.general_transformation(mr_2)
@gmt.randomized('n', gmt.RandInt(1, 10))
@gmt.fixed('c', 0)
def dummy_general_transformation(mtc: gmt.MetamorphicTestCase, n: int, c: int):
    followup = mtc.source_input + 2 * n * math.pi + c
    return followup


@gmt.relation(mr_1)
@gmt.randomized('n', gmt.RandInt(1, 10))
@gmt.fixed('c', 0)
def dummy_relation(source_output: float, followup_output: float, n: int, c: int):
    return source_output + n + c == pytest.approx(followup_output + n + c)


@gmt.general_relation(mr_2)
@gmt.randomized('n', gmt.RandInt(1, 10))
@gmt.fixed('c', 0)
def dummy_general_relation(mtc: gmt.MetamorphicTestCase, n: int, c: int):
    return mtc.source_output + n + c == pytest.approx(mtc.followup_output + n + c)


@pytest.mark.xfail()
@gmt.system_under_test(mr_1, mr_2)
def test_dummy_sut(input: float) -> float:
    return math.sin(input)


def test_framework_tests():
    KEY = get_test_file_name()
    assert test_results[KEY]['number_of_passed_tests'] == 20
    assert test_results[KEY]['number_of_failed_tests'] == 0
