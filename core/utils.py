import argparse
import os
from typing import Any, Dict

import numpy as np
from PIL import Image


class Utils:

    def __init__(self, parameters: Dict[str, Any]):
        self.canvas_size = parameters['canvas_size']
        self.count_vertices = parameters['count_vertices']
        self.target_image = None
        self.parameters = parameters

    def compute_polygon_count(self) -> int:
        """ Computes the number of polygons """

        polygon_count = self.count_vertices // 4

        return polygon_count

    def setup(self) -> None:

        self.check_directories()

        self.parameters["count_polygons"] = self.compute_polygon_count()

        self.parameters["target_image_str"] = 'target/' + self.parameters["target_image_str"] + '.bmp'

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
    def check_directories() -> None:
        """ Checks for the existence of given directories and creates them if they do not exist """

        if 'dump' not in os.listdir():
            os.mkdir('dump')

        for dir_ in ['log', 'img', 'temp']:
            if dir_ not in os.listdir('dump'):
                os.mkdir('dump/' + dir_)

    @staticmethod
    def parse_arguments() -> Any:
        """ Parses the command line arguments """
        parser = argparse.ArgumentParser(description='Approximate paintings with evolutionary algorithms')
        parser.add_argument('algo', type=str, help='Choose the algorithm to run', choices=['hc', 'ppa', 'sa'])
        parser.add_argument('run', type=int, help='Which run this is', choices=range(1, 6))
        parser.add_argument(
            'target_image', type=str, help='Which image to use', choices=(
                "mondriaan",
                "starry_night",
                "mona_lisa",
                "the_kiss",
                "bach",
                "the_persistence_of_memory",
                "convergence"
            )
        )
        args = parser.parse_args()

        return args
