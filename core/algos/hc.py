import os
from typing import Tuple, Any

from PIL.Image import Image

from core.algos.fitness import Fitness
from core.algos.mutations import Mutations
from core.algos.save import SaveResults
from core.constellation.constellations import Constellations
from core.utils import Utils


class Hc:
    """
    1. Generate a random polygon constellation
    2. Compute MSE for the individual
    3. Randomly mutate the individual
    4. Compute offspring MSE. If lower, offspring becomes new individual, else is discarded
    5. Back to step 2
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
        self.mutate = Mutations(self.canvas_size, self.count_polygons, self.count_vertices,
                                self.max_population_size, self.max_offspring_count)
        self.save = SaveResults(self.run_number, self.count_vertices, self.save_freq,
                                os.path.basename(self.target_image.filename)[:-4], self.algo)

    def run_hc(self) -> Any:
        """ Main hillclimber logic """

        print(f"Run {self.run_number}: Starting {self.algo} with {self.max_iterations} "
              f"iterations on {self.target_image.filename}")

        # 1. Generate a random polygon constellation
        individual = self.constellation.generate_random_polygon_constellation()

        for iteration in range(self.max_iterations):

            # 2. Compute MSE for the individual
            individual.mse = self.fitness.compute_mean_squared_error(individual.individual_as_array)

            if self.save_freq != 0 and iteration % self.save_freq == 0:
                self.save.save_csv(
                    iteration=iteration,
                    average_mse=individual.mse,
                )

            if iteration == 0 or iteration == self.max_iterations / 4 - 1 or iteration == self.max_iterations / 2 - 1 or iteration == (self.max_iterations / 4) * 3 - 1:
                self.save.save_images(iteration=iteration, individual=individual)

            # 3. Randomly mutate the individual
            offspring = self.mutate.randomly_mutate(individual, 1)

            # 4. Compute offspring MSE. If lower, offspring becomes new individual, else, compute chance of being discarded
            offspring.mse = self.fitness.compute_mean_squared_error(offspring.individual_as_array)

            if offspring.mse < individual.mse:
                individual = offspring

            # Last iteration save
            if iteration == self.max_iterations - 1:
                self.save.save_images(iteration=iteration, individual=individual)
                self.save.save_csv(
                    iteration=iteration,
                    average_mse=individual.mse,
                )
