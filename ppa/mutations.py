import math
import random
from functools import partial
from typing import Tuple

from constellation.constellations import Constellations
from models.constellation import Constellation
from models.polygon import Polygon


class Mutations:
    """ Contains all the functions pertaining to the mutation section of the PPA """

    def __init__(self,
                 canvas_size: Tuple[int, int],
                 count_polygons: int,
                 count_vertices: int,
                 max_population_size: int
                 ):
        self.canvas_size = canvas_size
        self.count_polygons = count_polygons
        self.count_vertices = count_vertices
        self.max_population_size = max_population_size

        self.mutation_options = [
            partial(self._move_vertex),
            partial(self._transfer_vertex),
            partial(self._change_drawing_index),
            partial(self._change_color)
        ]

    def randomly_mutate(self, individual: Constellation) -> Constellation:
        """
        Randomly selects a mutation option and applies it to the individual
        :param individual: The individual to be mutated
        :return: The mutated individual
        """

        new_individual = Constellations.copy_constellation(individual)

        for _ in range(individual.count_mutations):
            random_mutation = random.choice(self.mutation_options)

            new_individual = random_mutation(new_individual)

        return new_individual

    def compute_offspring_count(self, individual: Constellation) -> None:
        """
        Computes how many offsprings an individual should generate
        :param individual: The individual whose offspring count is to be computed
        :return: None
        """

        individual.count_offsprings = math.ceil(
            self.max_population_size * individual.fitness * random.random()
        )

    def compute_mutation_count(self, individual: Constellation) -> None:
        """
        Computes how many mutations an individual should apply on each offspring
        :param individual: The individual whose mutation count is to be computed
        :return: None
        """

        individual.count_mutations = math.ceil(
            (9 * self.count_vertices / 4
             ) * (
                    1 / self.max_population_size
            ) * 1 - individual.fitness * random.random()
        )

    def _move_vertex(self, individual: Constellation) -> Constellation:
        """
        Moves the vertex of a randomly selected Polygon
        :param individual: The list of candidate Polygons for a move
        :return: The list of Polygons with the mutated Polygon
        """

        chosen_polygon = self._choose_random_polygon(individual)

        chosen_vertex = random.choice(chosen_polygon.coordinates)
        idx_chosen_vertex = chosen_polygon.coordinates.index(chosen_vertex)

        new_vertex = self._choose_random_new_vertex()

        chosen_polygon.coordinates.remove(chosen_vertex)
        chosen_polygon.coordinates.insert(idx_chosen_vertex, new_vertex)

        return individual

    def _transfer_vertex(self, individual: Constellation) -> Constellation:
        """
        Moves a vertex to 'hide' it while keeping the count of vertices the same.
        :param individual: The list of candidate Polygons
        :return: The list of Polygons with the two mutated Polygons
        """

        polygon_1, polygon_2 = self._choose_two_random_polygons(individual)

        coordinates_to_transfer = random.choice(polygon_1.coordinates)

        polygon_1.coordinates.remove(coordinates_to_transfer)

        # Randomly choose a first coordinate on Polygon 2
        idx_first_coordinate_p2 = random.randint(0, len(polygon_2.coordinates) - 1)

        # Choose the next one in the index to create the vertex unless it is at the last index,
        # in which case choose the first coordinate in the index
        idx_second_coordinate_p2 = idx_first_coordinate_p2 + 1 if idx_first_coordinate_p2 != len(
            polygon_2.coordinates) - 1 else 0

        random_vertex_p2 = polygon_2.coordinates[idx_first_coordinate_p2], polygon_2.coordinates[
            idx_second_coordinate_p2]

        coordinates_to_transfer = self._find_midpoint(random_vertex_p2)

        polygon_2.coordinates.insert(idx_first_coordinate_p2 + 1, coordinates_to_transfer)

        return individual

    def _change_drawing_index(self, individual: Constellation) -> Constellation:
        """
        Randomly selects a Polygon and assigns it a new randomly selected drawing order
        :param individual: A list containing the Polygon objects in a constellation
        :return: A list of Polygon objects with the modified Polygon
        """

        chosen_polygon = self._choose_random_polygon(individual)
        new_idx = random.randint(0, self.count_polygons - 1)

        individual.individual_as_polygons.remove(chosen_polygon)
        individual.individual_as_polygons.insert(new_idx, chosen_polygon)

        return individual

    def _change_color(self, individual: Constellation) -> Constellation:
        """
        Randomly selects a polygon, an RGBA-channel and a new color, and switches the channel to that new color
        :param individual: A list containing the Polygon objects in a constellation
        :return: A list of Polygon objects with the modified Polygon
        """

        chosen_polygon = self._choose_random_polygon(individual)
        chosen_channel = random.randint(0, 3)
        random_new_color = random.randint(0, 255)

        chosen_polygon.color[chosen_channel] = random_new_color

        return individual

    def _choose_two_random_polygons(self, individual: Constellation) -> Tuple[Polygon, Polygon]:
        """
        Utility function randomly pickking two Polygons with some added checks (can't be the same Polygon twice and one
        of the Polygons must have at least 4 vertices
        :type individual: The list of Polygons to choose from
        :return: A tuple with the two selected Polygons
        """

        polygon_checks = False
        polygon_1 = []
        polygon_2 = []

        while not polygon_checks:
            polygon_1 = self._choose_random_polygon(individual)
            polygon_2 = self._choose_random_polygon(individual)

            if polygon_1 != polygon_2 and len(polygon_1.coordinates) >= 4:
                polygon_checks = True

        return polygon_1, polygon_2

    def _choose_random_new_vertex(self) -> Tuple[int, int]:
        """
        Utility function to randomly pick a new vertex
        :return: The new vertex
        """

        new_x, new_y = random.randint(0, self.canvas_size[0]), random.randint(0, self.canvas_size[1])

        return new_x, new_y

    @staticmethod
    def _choose_random_polygon(individual: Constellation) -> Polygon:
        """
        Utility function to choose a random Polygon
        :param individual: The list of Polygons to choose from
        :return: The selected Polygon
        """

        random_polygon = random.choice(individual.individual_as_polygons)

        return random_polygon

    @staticmethod
    def _find_midpoint(vertex: Tuple[Tuple[float, float], Tuple[float, float]]) -> Tuple[float, float]:
        """
        Utility function to find the midpoint on a vertex
        :param vertex: The vertex to find the midpoint on
        :return: The midpoint of the given vertex
        """

        x1, x2, y1, y2 = vertex[0][0], vertex[1][0], vertex[0][1], vertex[1][1]

        x_midpoint, y_midpoint = ((x1 + x2) / 2, (y1 + y2) / 2)

        return x_midpoint, y_midpoint
