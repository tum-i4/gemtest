import math
from typing import List

import pytest

import gemtest as gmt
from tests.end2end.conftest import test_results, get_test_file_name

mr_1 = gmt.create_metamorphic_relation(name='mr_1', data=range(10))
mr_2 = gmt.create_metamorphic_relation(name='mr_2', data=range(10))


@gmt.transformation(mr_1, mr_2)
def dummy_transformation(source_input: int):
    return source_input + 2 * math.pi, source_input + 4 * math.pi


@gmt.general_relation(mr_1, mr_2)
def dummy_relation(mtc: gmt.MetamorphicTestCase):
    return (mtc.source_output == pytest.approx(mtc.followup_outputs[0])
            and mtc.source_output == pytest.approx(mtc.followup_outputs[1]))


@gmt.system_under_test(mr_1, batch_size=0)
def test_dummy_sut_no_batch(input) -> float:
    assert isinstance(input, int) or isinstance(input, float)
    return math.sin(input)


@gmt.system_under_test(mr_1, batch_size=1)
def test_dummy_sut_smaller_batch_one(batch: List[float]) -> List[float]:
    assert isinstance(batch, list)
    assert len(batch) == 1
    return [math.sin(i) for i in batch]


@gmt.system_under_test(mr_1, batch_size=5)
def test_dummy_sut_smaller_batch(batch: List[float]) -> List[float]:
    assert isinstance(batch, list)
    assert len(batch) <= 5
    return [math.sin(i) for i in batch]


@gmt.system_under_test(mr_2, batch_size=20)
def test_dummy_sut_bigger_batch(batch: List[float]) -> List[float]:
    assert isinstance(batch, list)
    assert len(batch) <= 20
    return [math.cos(i) for i in batch]


def test_framework_tests():
    KEY = get_test_file_name()
    assert test_results[KEY]['number_of_passed_tests'] == 40
    assert test_results[KEY]['number_of_failed_tests'] == 0
