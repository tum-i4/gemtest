import importlib
import importlib.util
import sys
from pathlib import Path

from gemtest.conftest import get_conftest_config


def get_sut():
    sut_filepath = get_conftest_config().get("sut_filepath")
    sut_class = get_conftest_config().get("sut_class")
    return load_sut_from_path(filepath=Path(sut_filepath),
                              class_name=sut_class)


def load_module(filepath: Path):
    module_name = filepath.name
    spec = importlib.util.spec_from_file_location(module_name, filepath.resolve())
    if spec is not None:
        _spec = spec
        module = importlib.util.module_from_spec(_spec)
        sys.modules[module_name] = module
        assert _spec.loader is not None
        loader = _spec.loader
        loader.exec_module(module)
        return module
    raise ImportError(f"Couldn't find a module under: {filepath}")


def load_sut_from_path(filepath: Path, class_name="SUT"):
    sut_module = load_module(filepath)
    sut_obj = getattr(sut_module, class_name)
    return sut_obj()
