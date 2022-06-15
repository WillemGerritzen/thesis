from typing import List

from models.constellation import Constellation


class SortPopulation:

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


sort = SortPopulation()
