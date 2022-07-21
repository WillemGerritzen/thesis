import os.path
from typing import Tuple, Any

from PIL import Image

from core.algos.save import SaveResults
from core.constellation.constellations import Constellations
from core.statistics.cli import stats
from core.utils import Utils
from .fitness import Fitness
from .mutations import Mutations


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
            run_number: str,
            target_image_str: str,
            algo: str,
            max_offspring_count: int,
    ) -> None:
        self.canvas_size = canvas_size
        self.count_polygons = count_polygons
        self.max_population_size = max_population_size
        self.count_vertices = count_vertices
        self.target_image = target_image
        self.target_image_array = Utils.bitmap_to_array(self.target_image.filename)
        self.save_freq = save_freq
        self.max_iterations = max_iterations
        self.run_number = run_number
        self.target_image_str = target_image_str
        self.algo = algo
        self.max_offspring_count = max_offspring_count

        self.constellation = Constellations(self.canvas_size, self.count_vertices, self.count_polygons)
        self.fitness = Fitness(self.target_image_array, self.canvas_size)
        self.mutate = Mutations(self.canvas_size, self.count_polygons, self.count_vertices, self.max_population_size, self.max_offspring_count)
        self.save = SaveResults(self.run_number, self.count_vertices, self.save_freq,
                                os.path.basename(self.target_image.filename)[:-4], self.algo)

    def run_ppa(self) -> Any:
        """ Main PPA logic """
        population = [self.constellation.generate_random_polygon_constellation() for _ in
                      range(self.max_population_size)]

        print(
            f"Run {self.run_number}: Starting {self.algo} with {self.count_vertices} vertices on {self.target_image.filename[7:-4]}")

        offsprings = []
        current_save = 1
        count_generation = len(population)

        while count_generation < self.max_iterations:
            count_generation += len(offsprings)
            save_tracker = round(count_generation, -3)
            save = save_tracker != current_save
            population += offsprings

            # 2. Compute fitness of the whole population
            self.fitness.compute_population_fitness(population)

            # 3. Sort population and discard the worst individuals
            population = self.fitness.sort_population_by_fitness(population)[:self.max_population_size]

            if self.save_freq != 0 and save:
                current_save = save_tracker
                average_fitness = stats.compute_average_fitness(population)
                average_mse = stats.compute_average_mse(population)

                self.save.save_csv(
                    iteration=count_generation,
                    average_mse=average_mse,
                    average_fitness=average_fitness,
                    best_mse=population[0].mse,
                    best_fitness=population[0].fitness
                )

            if save_tracker == 0 or save_tracker == self.max_iterations / 4 or save_tracker == (self.max_iterations / 4) * 2 or save_tracker == (self.max_iterations / 4) * 3:
                self.save.save_images(iteration=count_generation, individual=population[0])

            # 4. Create offsprings
            offsprings = self.mutate.generate_offsprings(population)

            # Last generation save
            if count_generation >= self.max_iterations:
                self.save.save_images(iteration=count_generation, individual=population[0])
                self.save.save_csv(
                    iteration=count_generation,
                    average_mse=stats.compute_average_mse(population),
                    average_fitness=stats.compute_average_fitness(population),
                    best_mse=population[0].mse,
                    best_fitness=population[0].fitness
                )
