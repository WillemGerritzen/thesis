import math
import random
from copy import deepcopy
from typing import Tuple, Optional, List, Union

import numpy as np

from core.constellation.constellations import Constellations
from models.constellation import Constellation
from models.polygon import Polygon


class Mutations:
    """ Contains all the functions pertaining to the mutation section of the PPA """

    def __init__(
            self,
            canvas_size: Tuple[int, int],
            count_polygons: int,
            count_vertices: int,
            max_population_size: int,
            max_offspring_count: int,
            ffa: bool
    ):
        self.canvas_size = canvas_size
        self.count_polygons = count_polygons
        self.count_vertices = count_vertices
        self.max_population_size = max_population_size
        self.max_offspring_count = max_offspring_count
        self.ffa = ffa

        self.mutation_constant = 13 * count_vertices / 5
        self.max_vertices_per_polygon = (count_vertices // 4) + 3

        self.mutation_options = [
            self._move_vertex,
            self._transfer_vertex,
            self._change_drawing_index,
            self._change_color
        ]

        self.constellation = Constellations(self.canvas_size, self.count_vertices, self.count_polygons)

    def generate_offsprings(self, population: List[Constellation]) -> Union[List[Constellation], Tuple[List[Constellation], List[float]]]:
        """
        Generates the offsprings of the population
        :param population: The population of Constellation objects
        :return: The offsprings of the population
        """

        offsprings = []
        mse_lst = []

        for individual in population:
            offspring_count = self._compute_offspring_count(individual)
            mutation_count = self._compute_mutation_count(individual)

            for _ in range(offspring_count):
                offsprings.append(self.randomly_mutate(individual, mutation_count))

            if self.ffa:
                for offspring in offsprings:
                    mse_lst.append(offspring.mse)

        return offsprings, mse_lst

    def randomly_mutate(self, individual: Constellation, count_mutations: int) -> Constellation:
        """
        Randomly selects a mutation option and applies it to the individual
        :param count_mutations: How many mutations to apply
        :param individual: The individual to be mutated
        :return: The mutated individual
        """

        new_individual = deepcopy(individual)

        for _ in range(count_mutations):
            random_mutation = np.random.choice(self.mutation_options)

            new_individual = random_mutation(new_individual)

        self.constellation.draw_mutated_individual(new_individual)

        return new_individual

    def simulate_annealing(self, mse_diff: float, iteration_number: int) -> float:
        """
        Simulates annealing by computing the probability of a mutation based on the MSE difference and the temperature
        :param mse_diff: The MSE difference between the current and the previous generation
        :param iteration_number: The current iteration number
        :return: The probability of a mutation
        """

        temperature = self._compute_temperature(iteration_number)

        try:
            probability = math.exp(-mse_diff / temperature)
        except OverflowError:
            probability = 0

        return probability

    def _compute_offspring_count(self, individual: Constellation) -> int:
        """
        Computes how many offsprings an individual should generate
        :param individual: The individual whose offspring count is to be computed
        :return: How many offsprings the individual should generate
        """

        return math.ceil(self.max_offspring_count * individual.fitness * random.random())

    def _compute_mutation_count(self, individual: Constellation) -> int:
        """
        Computes how many mutations an individual should apply on each offspring
        :param individual: The individual whose mutation count is to be computed
        :return: How many mutations the individual should apply
        """

        return math.ceil(self.mutation_constant * (1 - individual.fitness) * random.random())

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
        Moves a vertex to 'hide' it while keeping the count of vertices the same within the run
        :param individual: The list of candidate Polygons
        :return: The list of Polygons with the two mutated Polygons
        """

        polygon_1, polygon_2 = self._choose_two_polygons(individual)

        vertex_to_delete = random.choice(polygon_1.coordinates)
        polygon_1.coordinates.remove(vertex_to_delete)

        vertex_1, vertex_2 = self._find_random_vertex_and_adjacent_vertex(polygon_2.coordinates)

        random_vertex = self._find_random_point((vertex_1, vertex_2))

        polygon_2.coordinates.insert(polygon_2.coordinates.index(vertex_1), random_vertex)

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

    def _choose_random_new_vertex(self) -> Tuple[int, int]:
        """
        Utility function to randomly pick a new vertex
        :return: The new vertex
        """

        new_x, new_y = random.randint(0, self.canvas_size[0]), random.randint(0, self.canvas_size[1])

        return new_x, new_y

    def _choose_two_polygons(self, individual: Constellation) -> Tuple[Polygon, Polygon]:
        """
        Chooses two different polygons where p1 can't be a triangle and p2 can't have the max number of vertices.
        Given this is the only place where vertices can move from one polygon to another, and that all polygons are
        intinalized with at least 3 and never more than the max number of vertices, there is no risk of max vertices
        count being exceeded.
        :type individual: The list of Polygons to choose from
        :return: A tuple with the two selected Polygons
        """

        available_polygons = individual.individual_as_polygons.copy()

        p1 = random.choice([polygon for polygon in available_polygons if len(polygon.coordinates) > 3])
        available_polygons.remove(p1)

        p2 = random.choice([polygon for polygon in available_polygons if len(polygon.coordinates) < self.max_vertices_per_polygon])

        return p1, p2

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
    def _compute_temperature(iteration_number: int) -> float:
        """
        Utility function to compute the temperature based on the iteration number
        :param iteration_number: The iteration number
        :return: The new temperature
        """
        temperature = 1000 * 0.99999 ** iteration_number

        return temperature

    @staticmethod
    def _find_random_point(vertex: Tuple[Tuple[float, float], Tuple[float, float]]) -> Optional[Tuple[float, float]]:
        """
        Utility function to find a random point on a line between two vertices
        :param vertex: The two vertices of the line
        :return: The point on the line
        """

        x1, x2, y1, y2 = vertex[0][0], vertex[1][0], vertex[0][1], vertex[1][1]

        if x1 != x2:  # If the line is not vertical, choose a random x between x1 and x2 and find the corresponding y
            new_x = random.uniform(x1, x2)
            slope = (y2 - y1) / (x2 - x1)
            intercept = (x1 * y2 - x2 * y1) / (x1 - x2)
            new_y = slope * new_x + intercept

        else:  # If the line is vertical or horizontal, choose x and y at random
            new_x = random.uniform(x1, x2)
            new_y = random.uniform(y1, y2)

        return new_x, new_y

    @staticmethod
    def _find_random_vertex_and_adjacent_vertex(
            polygon_coordinates: List[Tuple[float, float]]
    ) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        vertex_1 = random.choice(polygon_coordinates)
        adjacent_vertex_idx = random.choice([1, -1])

        try:
            vertex_2 = polygon_coordinates[polygon_coordinates.index(vertex_1) + adjacent_vertex_idx]

        except IndexError:
            if adjacent_vertex_idx == 1:
                vertex_2 = polygon_coordinates[0]
            else:
                vertex_2 = polygon_coordinates[-1]

        return vertex_1, vertex_2
