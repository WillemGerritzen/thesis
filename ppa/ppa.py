from typing import Tuple

from PIL import Image

from constellation.constellations import Constellations
from .fitness import Fitness
from .mutations import Mutations
from .utils import bitmap_to_array


class Ppa:
    """
    1. Generate random population of polygon constellations (Size = M)
    2. Compute MSE
    3. Sort population (keeping best M individuals)
    4. Create offsprings (each individual creates nr new individuals)
    5. Back to step 2.
    """

    def __init__(
            self,
            target_image: Image,
            canvas_size: Tuple[int, int],
            count_polygons: int,
            max_population_size: int,
            count_vertices: int,
            save_freq: int
    ):
        self.canvas_size = canvas_size
        self.count_polygons = count_polygons
        self.max_population_size = max_population_size
        self.count_vertices = count_vertices
        self.target_image = target_image
        self.target_image_array = bitmap_to_array(self.target_image.filename)
        self.save_freq = save_freq

        self.constellation = Constellations(self.canvas_size, self.count_vertices, self.count_polygons)
        self.fitness = Fitness(self.target_image_array)
        self.mutate = Mutations(self.canvas_size, self.count_polygons, self.count_vertices, self.max_population_size)

    def run_ppa(self):
        self._first_run_ppa()

    def _first_run_ppa(self):
        """
        Dictates the first run of the PPA
        :return: None
        """

        # 1. Generate random population of polygon constellations
        population = [self.constellation.generate_random_polygon_constellation() for _ in
                      range(self.max_population_size)]

        # 2. Compute fitness of the whole population
        self.fitness.compute_population_fitness(population)

        # 3. Sort population
        sorted_population = sorted(population, key=lambda indiv: indiv.fitness, reverse=True)

        # 4. Create offsprings
        for individual in sorted_population:
            if not individual.count_offsprings:
                self.mutate.compute_offspring_count(individual)

            if not individual.count_mutations:
                self.mutate.compute_mutation_count(individual)

            # Start generating offsprings
