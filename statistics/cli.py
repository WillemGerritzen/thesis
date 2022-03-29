from typing import List

from models.constellation import Constellation


class Statistics:

    @staticmethod
    def compute_average_fitness(population: List[Constellation]) -> float:
        """
        Computes the average fitness of the population.
        :param population: The population to compute the average fitness for.
        :return: The average fitness of the population.
        """
        all_fitness = tuple(individual.fitness for individual in population if individual.fitness is not None)

        if len(all_fitness) == 0:
            return 0.0

        sum_fitness = sum(all_fitness)
        average_fitness = sum_fitness / len(population)

        return average_fitness

    @staticmethod
    def compute_average_mse(population: List[Constellation]) -> float:
        """
        Computes the average MSE of the population.
        :param population: The population to compute the average MSE for.
        :return: The average MSE of the population.
        """

        all_mse = tuple(individual.mse for individual in population if individual.mse is not None)

        if len(all_mse) == 0:
            return 0.0

        sum_mse = sum(all_mse)
        average_mse = sum_mse / len(population)

        return average_mse


stats = Statistics()
