from pathlib import Path

import pytest

import gemtest
from gemtest.utils.sut_loader import load_sut_from_path, get_sut


class TestSUT:
    value = 1

    def execute(self):
        return self.value


def test_load_sut_from_path():
    sut = load_sut_from_path(Path(__file__), "TestSUT")
    assert 1 == sut.execute()


def test_wrong_class():
    with pytest.raises(AttributeError):
        load_sut_from_path(Path(__file__), "MissingSUT")


def test_wrong_path():
    with pytest.raises(FileNotFoundError):
        load_sut_from_path(Path("some_class.py"), "TestSUT")


def test_missing_module():
    with pytest.raises(ImportError):
        load_sut_from_path(Path("some_path"), "TestSUT")


@pytest.fixture
def setup_config(monkeypatch):
    with monkeypatch.context() as m:
        m.setitem(gemtest.conftest.CONFIG, "sut_filepath", __file__)
        m.setitem(gemtest.conftest.CONFIG, "sut_class", "TestSUT")
        yield


def test_get_sut(setup_config):
    sut = get_sut()
    assert 1 == sut.execute()
