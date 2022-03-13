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
            save_freq: int
    ):
        self.canvas_size = canvas_size
        self.count_polygons = count_polygons
        self.max_population_size = max_population_size
        self.target_image = target_image
        self.target_image_array = bitmap_to_array(self.target_image.filename)
        self.save_freq = save_freq

        self.constellation = Constellations(self.canvas_size, self.count_polygons)
        self.fitness = Fitness(self.target_image_array)
        self.mutate = Mutations(self.count_polygons)

    def run_ppa(self):
        self._first_run_ppa()

    def _first_run_ppa(self):
        """
        Dictates the first run of the PPA
        :return: None
        """

        # 1. Generate random population of polygon constellations
        all_constellations = [self.constellation.generate_random_polygon_constellation() for _ in range(self.max_population_size)]

        # Separate the Image objects from the Polygon objects since they're used differently
        population_as_images = [individual[0] for individual in all_constellations]
        population_as_polygons = [polygon[1] for polygon in all_constellations]

        # 2. Compute fitness of the whole population
        population_fitness = self.fitness.compute_population_fitness(population_as_images)  # Make it only contain the fitness, and sort both populations based on that list

        # 3. Sort population
        sorted_population_fitness = sorted(population_fitness, key=lambda individual: individual[1], reverse=True)
        sorted_population_as_polygons = [pop_poly for _, pop_poly in sorted(zip(sorted_population_fitness, population_as_polygons), key=lambda individual: individual[0][1], reverse=True)]
        print(sorted_population_as_polygons)

        # 4. Create offsprings
        individual_as_image, individual_as_polygons = population_as_images[0], population_as_polygons[0]
        # ImageShow.show(individual_as_image)
        mutated_individual = self.mutate.change_drawing_index(individual_as_polygons)
        self.constellation.replace_with_mutated_individual(mutated_individual)

