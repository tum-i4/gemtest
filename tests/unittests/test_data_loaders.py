import os

import cv2
import numpy as np
import pytest

from gemtest import load_image_resource
from gemtest.metamorphic_error import InvalidInputError

img_path = "img_test_data_loader.png"
img_data = np.ones((32, 32, 3), dtype=np.uint8)


@pytest.fixture
def setup_config():
    cv2.imwrite(img_path, img_data)
    yield
    os.remove(img_path)


def test_load_image_resource(setup_config):
    res = load_image_resource(img_path)
    assert np.array_equal(img_data, res)


def test_load_missing_image_resource():
    with pytest.raises(InvalidInputError):
        load_image_resource("img.txt")
