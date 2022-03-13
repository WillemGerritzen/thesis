import numpy as np
from PIL import Image


def bitmap_to_array(bitmap_file_name: str) -> np.ndarray:
    """
    Converts a bitmap file to a Numpy 2D array
    :param bitmap_file_name: The bitmap file to convert
    :return: A 2D array version of the bitmap file
    """

    with Image.open(bitmap_file_name) as img:
        # noinspection PyTypeChecker
        array = np.array(img)

    # Reshape 3D array to 2D for scikit to be able to use it
    nsamples, nx, ny = array.shape
    two_d_array = array.reshape((nsamples, nx * ny))

    return two_d_array


def image_object_to_array(image_obj: Image.Image) -> np.ndarray:
    """
    Converts an Image object to a Numpy 2D array
    :param image_obj: The Image object to be converted
    :return: The 2d array version of the Image object
    """

    # noinspection PyTypeChecker
    array = np.array(image_obj)

    # Reshape 3D array to 2D for scikit to be able to use it
    nsamples, nx, ny = array.shape
    two_d_array = array.reshape((nsamples, nx * ny))

    return two_d_array
