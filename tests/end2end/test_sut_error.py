import math

import pytest

import gemtest as gmt
from tests.end2end.conftest import test_results, get_test_file_name

mr_1 = gmt.create_metamorphic_relation(name='mr_1', data=range(10))


@gmt.transformation(mr_1)
def dummy_transformation(source_input: int):
    return source_input + 2 * math.pi


@gmt.relation(mr_1)
def dummy_relation(source_output: float, followup_output: float):
    return source_output == pytest.approx(followup_output)


@pytest.mark.xfail()
@gmt.system_under_test(mr_1)
def test_dummy_sut(input: float) -> float:
    if input == 1:
        try:
            # Raising an Error here and catching it to prevent SystemExit
            raise ValueError("test sut error")
        except ValueError as e:
            # Return a wrong value to fail the test
            return float("nan")


def test_framework_tests():
    KEY = get_test_file_name()
    assert test_results[KEY]['number_of_passed_tests'] == 9
    assert test_results[KEY]['number_of_failed_tests'] == 1
