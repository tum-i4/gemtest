import math
from typing import Any

import pytest

import gemtest as gmt
from gemtest import Visualizer


class VisualizerTest(Visualizer):
    def __init__(self, image_folder: str) -> None:
        super().__init__()
        self.image_folder = image_folder

    def visualize_input(self, sut_input: Any, **kwargs):
        pass

    def visualize_output(self, sut_input: Any, **kwargs):
        pass

def dummy_exporter():
    print("DummyExporter")
      

visualizer = VisualizerTest("some_folder")

mr_1 = gmt.create_metamorphic_relation(name='mr_1', data=range(10))
mr_2 = gmt.create_metamorphic_relation(name='mr_2', data=range(10))


@gmt.transformation(mr_1)
def dummy_transformation(source_input: int):
    return source_input + 2 * math.pi


@gmt.general_transformation(mr_2)
def dummy_transformation(mtc: gmt.MetamorphicTestCase):
    return mtc.source_input + 2 * math.pi


@gmt.relation(mr_1)
def dummy_relation(source_output: float, followup_output: float):
    return source_output == pytest.approx(followup_output)


@gmt.general_relation(mr_2)
def dummy_relation(mtc: gmt.MetamorphicTestCase):
    return mtc.source_output == pytest.approx(mtc.followup_output)


# This test file is used to run system tests for the framework with different command line
# options. Since this is a valid test file it is also executed on its own. Because it is
# marked with xfail this file itself will never cause a fails test in the pipeline.
@pytest.mark.xfail()
@gmt.system_under_test(mr_1, mr_2,
                       visualize_input=visualizer.visualize_input,
                       visualize_output=visualizer.visualize_output,
                       data_exporter = dummy_exporter
                       )
def test_dummy_sut_visualized(input: float) -> float:
    return math.sin(input)


@pytest.mark.xfail()
@gmt.system_under_test(mr_1, mr_2)
def test_dummy_sut(input: float) -> float:
    return math.sin(input)

@gmt.systems_under_test_dynamic()
def test_dummy_sut_dynamic(input: float, dummy_sut) -> float: 
    with dummy_sut:
        return dummy_sut.execute(input)


