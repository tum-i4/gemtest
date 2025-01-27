import os
import shutil
from pathlib import Path
from typing import Any
from unittest.mock import patch

import matplotlib.pyplot as plt
import numpy as np
import pytest

from gemtest.report.visualizer import Visualizer


class VisualizerTest(Visualizer):
    def __init__(self, image_folder: str) -> None:
        super().__init__()
        self.image_folder = image_folder

    def visualize_input(self, sut_input: Any, **kwargs):
        pass

    def visualize_output(self, sut_input: Any, **kwargs):
        pass


@pytest.fixture(scope="module")
def visualizer():
    # Create a temporary image folder for testing
    image_folder = "test_images"
    os.makedirs(image_folder, exist_ok=True)
    yield VisualizerTest(image_folder)
    # Clean up the temporary image folder
    shutil.rmtree("app/static/img/test_images")


def test_imsave(visualizer):
    # Generate a random image
    image = np.random.randint(0, 255, size=(100, 100, 3), dtype=np.uint8)
    image_name = "test_image.png"
    run_id = "test_run"

    # Call the imsave method
    relative_path = visualizer.imsave(image, visualizer.image_folder, image_name, run_id)
    expected_relative_path = str(Path("img/test_images/test_run/test_image.png"))
    assert relative_path == expected_relative_path

    # Assert that the image file exists
    full_path = Path(os.path.join("app/static", relative_path))
    assert full_path.is_file()


def test_imsave_error(visualizer, caplog):
    # Generate a random image
    image = "not_an_image"
    image_name = "test_image.png"
    run_id = "test_run"

    # Call the imsave method
    with pytest.raises(Exception):
        visualizer.imsave(image, visualizer.image_folder, image_name, run_id)


def test_savefig(visualizer):
    # Generate a random plot
    plt.plot([1, 2, 3, 4])
    image_name = "test_plot.png"
    run_id = "test_run"

    # Call the imsave method
    relative_path = visualizer.savefig(visualizer.image_folder, image_name, run_id)
    expected_relative_path = str(Path("img/test_images/test_run/test_plot.png"))
    assert relative_path == expected_relative_path

    # Assert that the image file exists
    full_path = Path(os.path.join("app/static", relative_path))
    assert full_path.is_file()


def test_savefig_error(visualizer, caplog):
    # Set up test data
    image_name = "test_image.png"
    run_id = "test_run"

    # Mock the savefig function to raise an exception
    with patch("matplotlib.pyplot.savefig") as mock_savefig:
        mock_savefig.side_effect = Exception("Mocked exception")

        # Call the savefig method
        with pytest.raises(Exception):
            visualizer.savefig(visualizer.image_folder, image_name, run_id)
