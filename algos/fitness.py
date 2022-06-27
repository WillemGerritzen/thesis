from typing import List, Tuple

import numpy as np

from models.constellation import Constellation
from utils import Utils


class Fitness:

    def __init__(self, target_image_array: np.ndarray, canvas_size: Tuple[int, int]):
        self.target_image_array = target_image_array
        self.canvas_size = canvas_size

    def compute_population_fitness(self, population: List[Constellation]) -> None:
        """
        Computes the fitness for a population
        :param population: The population to compute the fitness for
        :return: The population with each individual's fitness appended
        """

        self._compute_mse_for_population(population)

        mse_max = max(population, key=lambda indiv: indiv.mse).mse
        mse_min = min(population, key=lambda indiv: indiv.mse).mse

        for individual in population:
            if not individual.fitness:  # Avoid computing an already known value
                individual.fitness = self._compute_fitness(mse_max, mse_min, individual.mse)

    def compute_mean_squared_error(self, individual_array: np.ndarray) -> float:
        """
        Computes the MSE given an array of predicted values (the individual being evaluated) and an array of true
        values (the target image)
        :param individual_array: The individual being evaluated as an array
        :return: The mean squared error as a float
        """

        error = np.square(individual_array - self.target_image_array)
        mean_error = np.divide(error, self.canvas_size[0] * self.canvas_size[1])
        mse = np.sum(mean_error) * (255 ** 2)

        return mse

    def _compute_mse_for_population(self, population: List[Constellation]) -> None:
        """
        Iterates through a given population and computes the MSE for each individual
        :param population: The population to iterate through
        :return: A list consisting of the fitness value for each individual
        """

        for individual in population:
            if not individual.mse:  # Avoid computing an already known value
                individual.mse = self.compute_mean_squared_error(
                    Utils.image_object_to_array(individual.individual_as_image)
                )

    def _compute_fitness(self, mse_max: float, mse_min: float, mse_individual: float) -> float:
        """
        Computes the fitness and normalizes it
        :param mse_max: The highest mean squared error in the population
        :param mse_min: The lowest mean squared error in the population
        :param mse_individual: The mean squared error for the individual being evaluated
        :return: The normalized fitness value
        """

        fitness = (mse_max - mse_individual) / (mse_max - mse_min)

        normalized_fitness = self._normalize_fitness(fitness)

        return normalized_fitness

    @staticmethod
    def sort_population_by_fitness(population: List[Constellation], max_population_size: int) -> List[Constellation]:
        """
        Sort the population by fitness and delete the rest.
        :param population: The population to sort.
        :param max_population_size: The maximum population size.
        :return: The sorted population.
        """

        sorted_population = sorted(population, key=lambda individual: individual.fitness, reverse=True)

        del sorted_population[max_population_size:]

        return sorted_population

    @staticmethod
    def _normalize_fitness(fitness: float) -> float:
        """
        Normalizes the fitness value
        :param fitness: The fitness value to normalized
        :return: The normalized fitness value
        """

        normalized_fitness = 0.5 * (np.tanh(4 * (1 - fitness) - 2) + 1)

        return normalized_fitness
