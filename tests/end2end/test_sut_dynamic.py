from pathlib import Path

import pytest
from _pytest.monkeypatch import MonkeyPatch

import gemtest as gmt
from tests.end2end.conftest import test_results, get_test_file_name

mr_1 = gmt.create_metamorphic_relation(name='mr_1', data=range(10))


@gmt.transformation(mr_1)
def dummy_transformation(source_input: int):
    return source_input


@gmt.relation(mr_1)
def dummy_relation(source_output: float, followup_output: float):
    return source_output == pytest.approx(followup_output)


with MonkeyPatch().context() as m:
    m.setitem(gmt.conftest.CONFIG, "sut_filepath", str(Path(__file__).parent / "test_data" / "dynamic_sut.py"))
    m.setitem(gmt.conftest.CONFIG, "sut_class", "TestSUT")
    m.setitem(gmt.conftest.CONFIG, "is_sut_dynamic_active", True)


    @gmt.systems_under_test_dynamic(mr_1)
    def test_dummy_sut_dynamic(input: float, dynamic_sut) -> float:
        return dynamic_sut.execute(input)


    @gmt.system_under_test(mr_1)
    def test_dummy_sut(input: float) -> float:
        return input


@gmt.systems_under_test_dynamic(mr_1)
def test_dummy_sut_dynamic_not_set(input: float, dynamic_sut) -> float:
    return dynamic_sut.execute(input)


def test_framework_tests():
    KEY = get_test_file_name()
    assert test_results[KEY]['number_of_passed_tests'] == 10
    # two tests get skipped; if dynamic_sut is set normal sut decorator fails and if not dynamic_sut is set the
    # dynamic_sut decorator fails
    assert test_results[KEY]['number_of_failed_tests'] == 2
