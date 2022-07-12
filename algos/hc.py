import os
from typing import Tuple, Any

import cv2
from PIL.Image import Image

from algos.fitness import Fitness
from algos.mutations import Mutations
from algos.save import SaveResults
from constellation.constellations import Constellations
from utils import Utils


class HillClimber:
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
            experiment_name: str,
            target_image_str: str
    ) -> None:
        self.canvas_size = canvas_size
        self.count_polygons = count_polygons
        self.max_population_size = max_population_size
        self.count_vertices = count_vertices
        self.target_image = target_image
        self.target_image_array = Utils.bitmap_to_array(self.target_image.filename)
        self.save_freq = save_freq
        self.max_iterations = max_iterations
        self.experiment_name = experiment_name
        self.target_image_str = target_image_str

        self.constellation = Constellations(self.canvas_size, self.count_vertices, self.count_polygons)
        self.fitness = Fitness(self.target_image_array, self.canvas_size)
        self.mutate = Mutations(self.canvas_size, self.count_polygons, self.count_vertices,
                                self.max_population_size)
        self.save = SaveResults(self.experiment_name, self.count_vertices, self.save_freq,
                                os.path.basename(self.target_image.filename)[:-4], "HillClimber")

    def run_hc(self) -> Any:
        """ Main hillclimber logic """

        print(f"Run {self.experiment_name[-1]}: Starting Hillclimber with {self.max_iterations} "
              f"iterations on {self.target_image.filename}")

        # 1. Generate a random polygon constellation
        individual = self.constellation.generate_random_polygon_constellation()
        individual.count_mutations = 1
        individual.individual_as_array = cv2.cvtColor(Utils.image_object_to_array(individual.individual_as_image),
                                                      cv2.COLOR_BGR2RGB)
        for iteration in range(self.max_iterations):

            # 2. Compute MSE for the individual
            individual.mse = self.fitness.compute_mean_squared_error(individual.individual_as_array)

            if self.save_freq != 0 and iteration % self.save_freq == 0:
                self.save.save_csv(
                    iteration=iteration,
                    average_mse=individual.mse,
                )

            # 3. Randomly mutate the individual
            offspring = self.mutate.randomly_mutate(individual)
            self.constellation.draw_mutated_individual(offspring)
            new_array = cv2.cvtColor(Utils.image_object_to_array(offspring.individual_as_image), cv2.COLOR_BGR2RGB)

            # 4. Compute offspring MSE. If lower, offspring becomes new individual, else is discarded
            new_mse = self.fitness.compute_mean_squared_error(new_array)

            if new_mse < individual.mse:
                individual.mse = new_mse
                individual.individual_as_array = new_array
                self.save.save_images(iteration=iteration, population=[individual])
