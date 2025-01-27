from pathlib import Path

import cv2  # type: ignore
import numpy as np

from gemtest.metamorphic_error import InvalidInputError


def load_image_resource(input_path: str):
    """
    Load an image resource from a file path.

    Parameters
    ----------
    input_path : str
        The path to the image file to be loaded.

    Raises
    ------
    InvalidInputError
        If the file is not a valid image file.

    Returns
    -------
    np.ndarray
        The image loaded as a numpy array.
    """
    file_extension = Path(input_path).suffix.lower()
    # expand to more file formats if required
    if file_extension not in (".png", ".jpg", ".jpeg", ".ppm"):
        raise InvalidInputError(f"This data loader only supports lazy loading of .png, "
                                f".jpg, .jpeg and .ppm files. File at {input_path} is "
                                f"not supported.")
    image = cv2.imread(input_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return np.array(image_rgb)
