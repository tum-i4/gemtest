import math

import pytest

import gemtest as gmt
from tests.end2end.conftest import test_results, get_test_file_name

mr_1 = gmt.create_metamorphic_relation(name='mr_1', data=range(10))
mr_2 = gmt.create_metamorphic_relation(name='mr_2', data=range(10))


@gmt.transformation(mr_1, mr_2)
def dummy_transformation(source_input: int):
    return source_input + 2 * math.pi


@gmt.relation(mr_1, mr_2)
def dummy_relation(source_output: float, followup_output: float):
    return source_output == pytest.approx(followup_output)


@pytest.mark.xfail()
@gmt.system_under_test(mr_1)
def test_dummy_sut(input: float) -> float:
    return math.sin(input)


@pytest.mark.xfail()
@gmt.system_under_test(mr_2)
def test_dummy_sut_2(input: float) -> float:
    return math.cos(input)


def test_framework_tests():
    KEY = get_test_file_name()
    assert test_results[KEY]['number_of_passed_tests'] == 20
    assert test_results[KEY]['number_of_failed_tests'] == 0
