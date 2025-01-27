import math

import pytest

import gemtest as gmt
from tests.end2end.conftest import test_results, get_test_file_name

mr_1 = gmt.create_metamorphic_relation(name='mr_1',
                                       data=range(-10, 10),
                                       testing_strategy=gmt.TestingStrategy.SAMPLE,
                                       number_of_test_cases=20,
                                       number_of_sources=2)


@gmt.general_transformation(mr_1)
@gmt.randomized('n', gmt.RandInt(1, 10))
@gmt.fixed('c', 0)
def shift(mtc: gmt.MetamorphicTestCase, n: int, c: int):
    followup_input_1 = mtc.source_inputs[0] + 2 * n * math.pi + c
    followup_input_2 = mtc.source_inputs[1] - 2 * n * math.pi + c
    return followup_input_1, followup_input_2


@gmt.general_relation(mr_1)
def approximately_equals(mtc: gmt.MetamorphicTestCase) -> bool:
    return gmt.approximately(mtc.source_outputs[0], mtc.followup_outputs[0]) \
        and gmt.approximately(mtc.source_outputs[1], mtc.followup_outputs[1])


@pytest.mark.xfail()
@gmt.system_under_test(mr_1)
def test_dummy_sut(x: float) -> float:
    return math.sin(x)


def test_framework_tests():
    KEY = get_test_file_name()
    assert test_results[KEY]['number_of_passed_tests'] == 20
    assert test_results[KEY]['number_of_failed_tests'] == 0
