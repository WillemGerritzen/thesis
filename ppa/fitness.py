from typing import List, Tuple

import numpy as np
from PIL import Image
from sklearn.metrics import mean_squared_error

from .utils import image_object_to_array


class Fitness:

    def __init__(self, target_image_array: np.ndarray):
        self.target_image_array = target_image_array

    def compute_population_fitness(self, population: List[Image.Image]) -> List[Tuple[Image.Image, float]]:
        """
        Computes the fitness for a population
        :param population: The population to compute the fitness for
        :return: The population with each individual's fitness appended
        """

        mse_population = self._compute_mse_for_population(population)

        mse_max = max(mse_population)
        mse_min = min(mse_population)

        population_fitness = [
            (
                individual,
                self._compute_fitness(
                    mse_max,
                    mse_min,
                    mse_individual
                )
            ) for mse_individual, individual in zip(
                mse_population,
                population
            )
        ]

        return population_fitness

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

    def _compute_mse_for_population(self, population: List) -> List[float]:
        """
        Iterates through a given population and computes the MSE for each individual
        :param population: The population to iterate through
        :return: A list comprising of the fitness value for each individual
        """

        mse_population = [
            self._compute_mean_squared_error(image_object_to_array(individual)) for individual in population
        ]

        return mse_population

    def _compute_mean_squared_error(self, individual_array: np.ndarray) -> float:
        """
        Computes the MSE given an array of predicted values (the individual being evaluated) and an array of true
        values (the target image)
        :param individual_array: The individual being evaluated as an array
        :return: The mean squared error as a float
        """

        mse = mean_squared_error(self.target_image_array, individual_array)

        return mse

    @staticmethod
    def _normalize_fitness(fitness: float) -> float:
        """
        Normalizes the fitness value
        :param fitness: The fitness value to normalized
        :return: The normalized fitness value
        """

        normalized_fitness = 0.5 * (np.tanh(4 * (1 - fitness) - 2) + 1)

        return normalized_fitness
