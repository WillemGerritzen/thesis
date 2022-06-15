import os
from typing import Tuple, Any

from PIL.Image import Image

from algos.fitness import Fitness
from algos.mutations import Mutations
from algos.save import SaveResults
from constellation.constellations import Constellations
from utils import Utils


class HillClimber:
    """

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
                                os.path.basename(self.target_image.filename)[:-4])

    def run_hc(self) -> Any:
        """ Main hillclimber logic """

        print(f"Starting Hillclimber with {self.max_iterations} iterations on {self.target_image.filename}")

        # 1. Generate a random polygon constellation
        individual = self.constellation.generate_random_polygon_constellation()

        for iteration in range(self.max_iterations):
            print("----------------------------------")
            print(f"Starting iteration {iteration}")
            print("----------------------------------")

            # 2. Compute MSE for the individual
            individual.mse = self.fitness.compute_mean_squared_error(
                Utils.image_object_to_array(individual.individual_as_image)
            )

            print(f"Current MSE: {individual.mse}")

            # 3. Randomly mutate the individual
            offspring = self.mutate.randomly_mutate(individual)

            # 4. Compute offspring MSE. If lower, offspring becomes new individual, else is discarded
            offspring.mse = self.fitness.compute_mean_squared_error(Utils.image_object_to_array(offspring.individual_as_image))

            if offspring.mse < individual.mse:
                individual = offspring
                print(f"Found better MSE: {individual.mse}")


