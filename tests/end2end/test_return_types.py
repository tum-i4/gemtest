from typing import List, Tuple

import gemtest as gmt
from tests.end2end.conftest import test_results, get_test_file_name

mr_1 = gmt.create_metamorphic_relation(name='mr_1', data=range(10))


@gmt.general_transformation(mr_1)
def dummy_transformation(mtc: gmt.MetamorphicTestCase):
    assert len(mtc.source_inputs) == len(mtc.source_outputs)
    return mtc.source_outputs


@gmt.general_relation(mr_1)
def dummy_relation(mtc: gmt.MetamorphicTestCase):
    assert len(mtc.followup_inputs) == len(mtc.followup_outputs)
    return True


@gmt.system_under_test(mr_1)
def test_sut_no_batching_tuple(x: int) -> Tuple[int, int]:
    return x, x


@gmt.system_under_test(mr_1)
def test_sut_no_batching_list(x: int) -> List[int]:
    return [x, x]


@gmt.system_under_test(mr_1)
def test_sut_no_batching_none(x: int) -> None:
    return None


@gmt.system_under_test(mr_1, batch_size=10)
def test_sut_batching_tuple(batch: List[int]) -> List[Tuple[int, int]]:
    return [(x, x) for x in batch]


@gmt.system_under_test(mr_1, batch_size=10)
def test_sut_batching_list(batch: List[int]) -> List[List[int]]:
    return [[x, x] for x in batch]


@gmt.system_under_test(mr_1, batch_size=10)
def test_sut_batching_none(batch: List[int]) -> List[None]:
    return [None for _ in batch]


def test_framework_tests():
    KEY = get_test_file_name()
    assert test_results[KEY]['number_of_passed_tests'] == 6 * 10
    assert test_results[KEY]['number_of_failed_tests'] == 0
