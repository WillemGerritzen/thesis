import os
from typing import Tuple

import numpy as np
from PIL import Image

from exception_handling import ResizingError


class Utils:

    def __init__(self, canvas_size: Tuple[int, int], target_image_name: str, count_vertices: int):
        self.canvas_size = canvas_size
        self.target_image_name = target_image_name
        self.count_vertices = count_vertices
        self.target_image = None

    def compute_polygon_count(self) -> int:
        """ Computes the number of polygons """

        polygon_count = self.count_vertices // 4

        return polygon_count

    def validate_target_image(self) -> None:
        """ Validates the target image to ensure it can be used safely """

        self._check_image_existence()
        if not self.target_image:
            raise FileNotFoundError(f"Target image ({self.target_image_name}) not found!")

        self._check_extension()

        if self.target_image.size != self.canvas_size:
            mode = self._determine_mode()

            if mode == 'portrait':
                converted_image = self.target_image.resize((self.canvas_size[1], self.canvas_size[0]))
            elif mode == 'landscape':
                converted_image = self.target_image.resize((self.canvas_size[0], self.canvas_size[1]))
            else:
                raise ResizingError("Something went wrong when resizing the image")

            converted_image.save(self.target_image.filename)

            converted_image.close()
            self.target_image.close()

    def _check_image_existence(self) -> None:
        """ Checks the target image can be found and loads it """

        extensions = ['.jpg', '.png', '.bmp']
        for extension in extensions:
            if self.target_image_name + extension in os.listdir('img/target'):
                self.target_image = Image.open('img/target/' + self.target_image_name + extension)

    def _determine_mode(self) -> str:
        """
        Checks whether the target image is in portrait or landscape mode
        :return: The target image mode as a string
        """

        if self.target_image.width < self.target_image.height:
            return 'portrait'

        return 'landscape'

    def _check_extension(self) -> None:
        """ Converts the target image to a bitmap file if it is in a different format """
        if not self.target_image.filename.lower().endswith('.bmp'):
            self.target_image.save(self.target_image.filename[:-4] + '.bmp', format='BMP')
            os.remove(self.target_image.filename)

    @staticmethod
    def bitmap_to_array(bitmap_file_name: str) -> np.ndarray:
        """
        Converts a bitmap file to a Numpy 2D array
        :param bitmap_file_name: The bitmap file to convert
        :return: A 2D array version of the bitmap file
        """

        with Image.open(bitmap_file_name) as img:

            # noinspection PyTypeChecker
            array = np.array(img)

        return array

    @staticmethod
    def image_object_to_array(image_obj: Image.Image) -> np.ndarray:
        """
        Converts an Image object to a Numpy 2D array
        :param image_obj: The Image object to be converted
        :return: The 2d array version of the Image object
        """

        # noinspection PyTypeChecker
        array = np.array(image_obj)

        return array

    @staticmethod
    def check_directories():
        """ Checks for the existence of given directories and creates them if they do not exist """
        if 'img' not in os.listdir():
            os.mkdir('img')

        if 'temp' not in os.listdir('img'):
            os.mkdir('img/temp')

        if 'results' not in os.listdir():
            os.mkdir('results')



