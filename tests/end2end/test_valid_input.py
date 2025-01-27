import math

import pytest

import gemtest as gmt
from tests.end2end.conftest import test_results, get_test_file_name


def predefined_dummy_valid_input(y: float) -> bool:
    return y > 0


mr_1 = gmt.create_metamorphic_relation(name='mr_1',
                                       data=range(10),
                                       valid_input=predefined_dummy_valid_input
                                       )

mr_2 = gmt.create_metamorphic_relation(name='mr_2', data=range(10))


@gmt.transformation(mr_1)
def dummy_transformation(source_input: int):
    return source_input + 2 * math.pi


@gmt.relation(mr_1)
def dummy_relation(source_output: float, followup_output: float):
    return source_output == pytest.approx(followup_output)


@gmt.general_transformation(mr_2)
def dummy_transformation(mtc: gmt.MetamorphicTestCase):
    return mtc.source_input + 2 * math.pi


@gmt.general_relation(mr_2)
def dummy_relation(mtc: gmt.MetamorphicTestCase):
    return mtc.source_output == pytest.approx(mtc.followup_output)


@gmt.valid_input(mr_2)
def dummy_valid_input(y: float) -> bool:
    return y > 0


@pytest.mark.xfail()
@gmt.system_under_test()
def test_dummy_sut(input: float) -> float:
    return math.sin(input)


def test_framework_tests():
    KEY = get_test_file_name()
    assert test_results[KEY]['number_of_passed_tests'] == 12
    # tests with an invalid input get marked as skipped, just like xfailed tests,
    # therefore they are falling under failed in this statistic
    assert test_results[KEY]['number_of_failed_tests'] == 8
