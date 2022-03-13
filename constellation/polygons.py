from random import randint
from typing import Tuple, List

from PIL import Image

from constellation.polygon import Polygon


class PolygonGenerator:
    """ Class containing all the methods pertaining to polygon generation """

    def __init__(self, canvas: Image, count_polygons: int):
        self.canvas = canvas
        self.count_polygons = count_polygons

    def generate_polygons(self) -> List[Polygon]:
        """
        Generates a sequence of polygons
        :return: A tuple filled with the list of the coordinates of the nodes of each polygon
        """

        all_polygons = [self._generate_polygon(vertices=3) for _ in range(self.count_polygons)]

        return all_polygons

    def _generate_coordinate(self) -> Tuple[int, int]:
        """
        Generates random coordinates on the x- and y-axis
        :return: A tuple of x-y coordinates
        """
        x, y = randint(0, self.canvas.size[0]), randint(0, self.canvas.size[1])

        return x, y

    def _generate_polygon(self, vertices: int = 3) -> Polygon:
        """
        Generates a Polygon object given a number of vertices
        :param vertices: Determines how many edges the polygon has
        :return: An instantiated Polygon object with coordinates and color
        """

        polygon = Polygon()

        for _ in range(vertices):
            polygon.coordinates = [self._generate_coordinate() for _ in range(vertices)]

        polygon.color = self._generate_color()

        return polygon

    @staticmethod
    def _generate_color() -> List[int]:
        """
        Randomly picks colors (RGBA) for each polygon
        :return: A tuple of RGBA tuples
        """
        color = [randint(0, 255) for _ in range(4)]

        return color
