import random
from random import randint
from typing import Tuple, List

from PIL.Image import Image

from models.constellation import Constellation
from models.polygon import Polygon


class PolygonGenerator:
    """ Class containing all the methods pertaining to polygon generation """

    def __init__(self, canvas: Image, count_polygons: int, count_vertices: int):
        self.canvas = canvas
        self.count_polygons = count_polygons
        self.count_vertices = count_vertices

    def generate_polygons(self, initial_vertices: int = 3) -> Constellation:
        """
        Generates a sequence of polygons
        :return: A tuple filled with the list of the coordinates of the nodes of each polygon
        """

        all_polygons = [self._generate_polygon(initial_vertices=initial_vertices) for _ in range(self.count_polygons)]

        vertices_left = self.count_vertices - (initial_vertices * self.count_polygons)

        final_polygons = self._distribute_remaining_vertices(all_polygons, vertices_left)

        constellation = Constellation(final_polygons)

        return constellation

    def _generate_coordinate(self) -> Tuple[int, int]:
        """
        Generates random coordinates on the x- and y-axis
        :return: A tuple of x-y coordinates
        """
        x, y = randint(0, self.canvas.size[0]), randint(0, self.canvas.size[1])

        return x, y

    def _generate_polygon(self, initial_vertices: int = 3) -> Polygon:
        """
        Generates a Polygon object given a number of vertices
        :param initial_vertices: Determines how many edges the polygon has
        :return: An instantiated Polygon object with coordinates and color
        """

        coordinates = [self._generate_coordinate() for _ in range(initial_vertices)]

        color = self._generate_color()

        polygon = Polygon(coordinates, color)

        return polygon

    def _distribute_remaining_vertices(self, polygons: List[Polygon], remaining_vertices: int) -> List[Polygon]:
        """
        Randomly distributes the remaining vertices to the Polygons after their initial generation
        :param polygons: The list of Polygons to assign the remaining vertices to
        :param remaining_vertices: The count of vertices left to assign
        :return: The list of Polygons with the added vertices
        """

        for _ in range(remaining_vertices):
            random_polygon = random.choice(polygons)
            additional_vertex = self._generate_coordinate()
            random_polygon.coordinates.append(additional_vertex)

        return polygons

    @staticmethod
    def _generate_color() -> List[int]:
        """
        Randomly picks colors (RGBA) for each polygon
        :return: A tuple of RGBA tuples
        """
        color = [randint(0, 255) for _ in range(4)]

        return color
