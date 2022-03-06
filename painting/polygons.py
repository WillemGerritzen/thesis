from random import randint
from typing import Tuple, List

from PIL import Image


class Polygon:
    """ Class containing all the methods pertaining to polygon generation """

    def __init__(self, canvas: Image, count_polygons: int = 100):
        self.canvas = canvas
        self.count_polygons = count_polygons

    def generate_coordinates(self) -> Tuple[int, int]:
        """
        Generates coordinates on the x- and y-axis
        :return: A tuple of x-y coordinates
        """
        x, y = randint(0, self.canvas.size[0]), randint(0, self.canvas.size[1])

        return x, y

    def generate_polygon(self, vertices: int = 3) -> List[Tuple[int, int]]:
        """
        Generates a polygon given a number of vertices
        :param vertices: Determines how many edges the polygon has
        :return: A list of tuples contiaining the coordinates of each nod of the polygon
        """
        polygon = []

        for vertex in range(vertices):
            polygon.append(self.generate_coordinates())

        return polygon

    def generate_polygons(self) -> Tuple[List[Tuple[int, int]], ...]:
        """
        Generates a sequence of polygons
        :return: A tuple filled with the list of the coordinates of the nodes of each polygon
        """
        all_polygons = tuple(self.generate_polygon(vertices=3) for _ in range(self.count_polygons))

        return all_polygons

    def generate_colors(self) -> Tuple[Tuple[int, int, int, int], ...]:
        """
        Randomly picks colors (RGBA) for each polygon
        :return: A tuple of RGBA tuples
        """
        color = tuple(
            (randint(0, 255), randint(0, 255), randint(0, 255), randint(0, 255)) for _ in range(self.count_polygons))

        return color
