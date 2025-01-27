import logging
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt  # type: ignore


class Visualizer(ABC):
    """
    Visualizer class for the keypoint prediction.
    """

    def __init__(self) -> None:
        self.logger: logging.Logger = logging.getLogger(__name__)
        self.logger.addHandler(logging.StreamHandler())

    @abstractmethod
    def visualize_input(self, sut_input: Any, **kwargs):
        """
        Use this function to visualize an individual input to the system under test.

        Parameters
        ----------
        sut_input : Any
            The input to the system under test that should be visualized.
        **kwargs : dict
            index : int
                The index of the input in the list of inputs.
            run_id : str
                Identifier for the current test run.
            mtc: MetamorphicTestCase
                The metamorphic test case object that the sut_input belongs to.
        """

    @abstractmethod
    def visualize_output(self, sut_output: Any, **kwargs):
        """
        Use this function to visualize the output of the system under test.
        Implement a custom function to create an image from the sut_output and
        sut_input (if required), then use the provided Visualizer.save_image function
        to save the image and return the path.

        Parameters
        ----------
        sut_output : Any
            The output of the system under test that should be visualized.
        **kwargs : dict
            index : int
                The index of the input in the list of inputs.
            run_id : str
                Identifier for the current test run.
            mtc: MetamorphicTestCase
                The metamorphic test case object that the sut_input belongs to.
        """

    @staticmethod
    def imsave(image: Any, image_folder: str, image_name: str, run_id: str):
        base_dir = Path(os.path.join("app/static/img", image_folder, run_id))
        base_dir.mkdir(parents=True, exist_ok=True)
        path: Path = base_dir / image_name
        plt.imsave(path, image)
        return str(path.relative_to('app/static'))

    @staticmethod
    def savefig(image_folder: str, image_name: str, run_id: str):
        base_dir = Path(os.path.join("app/static/img", image_folder, run_id))
        base_dir.mkdir(parents=True, exist_ok=True)
        path: Path = base_dir / image_name
        plt.savefig(path, bbox_inches="tight", pad_inches=0)
        return str(path.relative_to('app/static'))
