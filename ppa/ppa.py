from typing import Tuple

from PIL import Image

from constellation.constellations import Constellations
from ppa.save import SaveResults
from statistics.cli import stats
from utils import Utils
from .fitness import Fitness
from .mutations import Mutations
from .sortpopulation import sort


class Ppa:
    """
    1. Generate random population of polygon constellations (Size = M)
    2. Compute MSE
    3. Sort population (keeping best M individuals)
    4. Create offsprings
        - Each individual creates nr new individuals with mr mutations per offspring per individual
    5. Back to step 2.
    """

    def __init__(
            self,
            target_image: Image,
            canvas_size: Tuple[int, int],
            count_polygons: int,
            max_population_size: int,
            count_vertices: int,
            save_freq: int,
            max_iterations: int,
            experiment_name: str
    ):
        self.canvas_size = canvas_size
        self.count_polygons = count_polygons
        self.max_population_size = max_population_size
        self.count_vertices = count_vertices
        self.target_image = target_image
        self.target_image_array = Utils.bitmap_to_array(self.target_image.filename)
        self.save_freq = save_freq
        self.max_iterations = max_iterations
        self.experiment_name = experiment_name

        self.constellation = Constellations(self.canvas_size, self.count_vertices, self.count_polygons)
        self.fitness = Fitness(self.target_image_array)
        self.mutate = Mutations(self.canvas_size, self.count_polygons, self.count_vertices, self.max_population_size)
        self.save = SaveResults(self.experiment_name, self.count_vertices, self.save_freq)

    def run_ppa(self):
        """ Main PPA logic """

        print(f"Starting PPA with {self.max_iterations} iterations")

        # 1. Generate random population of polygon constellations
        population = [self.constellation.generate_random_polygon_constellation() for _ in
                      range(self.max_population_size)]

        for iteration in range(self.max_iterations):

            print("----------------------------------")
            print(f"Starting iteration {iteration}")
            print("----------------------------------")

            # 2. Compute fitness of the whole population
            self.fitness.compute_population_fitness(population)

            # 3. Sort population
            sorted_population = sort.sort_population_by_fitness(population, self.max_population_size)

            average_fitness = stats.compute_average_fitness(sorted_population)
            average_mse = stats.compute_average_mse(sorted_population)

            print(f"Average fitness: {average_fitness}")
            print(f"Average MSE: {average_mse}\n")

            if self.save_freq != 0 and iteration % self.save_freq == 0:
                self.save.save_csv(iteration, average_fitness, average_mse)
                self.save.save_images(iteration, sorted_population)

            # 4. Create offsprings
            for count, individual in enumerate(sorted_population):
                if not individual.count_offsprings:
                    self.mutate.compute_offspring_count(individual)

                if not individual.count_mutations:
                    self.mutate.compute_mutation_count(individual)

                for _ in range(individual.count_offsprings):
                    offspring = self.mutate.randomly_mutate(individual)
                    self.constellation.draw_mutated_individual(offspring)
                    population.append(offspring)
