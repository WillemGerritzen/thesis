import numpy as np
from PIL import Image


class Utils:

    @staticmethod
    def bitmap_to_array(bitmap_file_name: str) -> np.ndarray:
        with Image.open(bitmap_file_name) as img:
            array = np.array(img)

            # Reshape 3d array to 2d for scikit to be able to use it
            nsamples, nx, ny = array.shape
            two_d_array = array.reshape((nsamples, nx * ny))
            
            return two_d_array


utils = Utils()
