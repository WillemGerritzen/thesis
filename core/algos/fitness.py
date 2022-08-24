import math
from typing import List, Tuple, Dict

import numpy as np

from core.utils import Utils
from models.constellation import Constellation


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
        mse_diff = mse_max - min(population, key=lambda indiv: indiv.mse).mse

        for individual in population:
            individual.fitness = self._compute_fitness(mse_max, mse_diff, individual.mse)

    def compute_mean_squared_error(self, individual_array: np.ndarray) -> float:
        """
        Computes the MSE given an array of predicted values (the individual being evaluated) and an array of true
        values (the target image)
        :param individual_array: The individual being evaluated as an array
        :return: The mean squared error as a float
        """

        error = np.square(individual_array.astype(np.float32) - self.target_image_array.astype(np.float32))
        mean_error = np.divide(error, self.canvas_size[0] * self.canvas_size[1])
        mse = float(np.sum(mean_error))

        return mse

    def _compute_mse_for_population(self, population: List[Constellation]) -> None:
        """
        Iterates through a given population and computes the MSE for each individual
        :param population: The population to iterate through
        :return: A list consisting of the fitness value for each individual
        """

        for individual in population:
            individual.mse = self.compute_mean_squared_error(
                Utils.image_object_to_array(individual.individual_as_image))

    def _compute_fitness(self, mse_max: float, mse_diff: float, mse_individual: float) -> float:
        """
        Computes the fitness and normalizes it
        :param mse_max: The highest mean squared error in the population
        :param mse_diff: The difference between the highest and lowest mean squared error in the population
        :param mse_individual: The mean squared error for the individual being evaluated
        :return: The normalized fitness value
        """

        fitness = (mse_max - mse_individual) / mse_diff

        normalized_fitness = self._normalize_fitness(fitness)

        return normalized_fitness

    @staticmethod
    def sort_population_by_fitness(population: List[Constellation]) -> List[Constellation]:
        """
        Sort the population by fitness and delete the rest.
        :param population: The population to sort.
        :return: The sorted population.
        """

        sorted_population = sorted(population, key=lambda individual: individual.fitness, reverse=True)

        return sorted_population

    @staticmethod
    def _normalize_fitness(fitness: float) -> float:
        """
        Normalizes the fitness value
        :param fitness: The fitness value to normalized
        :return: The normalized fitness value
        """

        normalized_fitness = 0.5 * (math.tanh(4 * fitness - 2) + 1)

        return normalized_fitness

    @staticmethod
    def sort_population_by_fitness_frequency(population: List[Constellation], mse_dict: Dict) -> List[Constellation]:
        """
        Sort the population by fitness frequency and delete the rest.
        :param mse_dict: The dictionary of mean squared errors.
        :param population: The population to sort.
        :return: The sorted population.
        """

        sorted_population = sorted(population, key=lambda x: mse_dict[x.mse])

        return sorted_population
