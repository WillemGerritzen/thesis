import os.path
import pickle
from datetime import datetime, timedelta
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
            algo: str
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

        self.constellation = Constellations(self.canvas_size, self.count_vertices, self.count_polygons)
        self.fitness = Fitness(self.target_image_array, self.canvas_size)
        self.mutate = Mutations(self.canvas_size, self.count_polygons, self.count_vertices, self.max_population_size)
        self.save = SaveResults(self.run_number, self.count_vertices, self.save_freq,
                                os.path.basename(self.target_image.filename)[:-4], self.algo)

    def run_ppa(self) -> Any:
        """ Main PPA logic """
        start_time = datetime.now()

        try:
            population, iterations = pickle.load(
                open(f"dump/temp/{self.run_number}_{self.algo}_{self.target_image.filename[7:-4]}.pkl", "rb"))

            print(
                f"Run {self.run_number}: Continuing {self.algo} with {self.max_iterations - iterations} iterations left on {self.target_image.filename[7:-4]}")

        except FileNotFoundError:
            population = [self.constellation.generate_random_polygon_constellation() for _ in
                          range(self.max_population_size)]
            iterations = 0
            print(
                f"Run {self.run_number}: Starting {self.algo} with {self.max_iterations} iterations on {self.target_image.filename[7:-4]}")

        offsprings = []

        for iteration in range(iterations, self.max_iterations):
            population += offsprings

            diff = datetime.now() - start_time
            if diff >= timedelta(hours=119):
                pickle.dump((population, iteration),
                            open(f"dump/temp/{self.run_number}_{self.algo}_{self.target_image.filename[7:-4]}.pkl",
                                 "wb+"))
                print("Hit time limit, saving...")
                exit(0)

            # 2. Compute fitness of the whole population
            self.fitness.compute_population_fitness(population)

            # 3. Sort population and discard the worst individuals
            population = self.fitness.sort_population_by_fitness(population)[:self.max_population_size]

            if self.save_freq != 0 and iteration % self.save_freq == 0:
                average_fitness = stats.compute_average_fitness(population)
                average_mse = stats.compute_average_mse(population)

                self.save.save_csv(
                    iteration=iteration,
                    average_mse=average_mse,
                    average_fitness=average_fitness,
                    best_mse=population[0].mse,
                    best_fitness=population[0].fitness
                )

            if iteration == 0 or iteration == self.max_iterations / 4 - 1 or iteration == (self.max_iterations / 4) * 2 - 1 or iteration == (self.max_iterations / 4) * 3 - 1:
                self.save.save_images(iteration=iteration, individual=population[0])

            # 4. Create offsprings
            offsprings = self.mutate.generate_offsprings(population)

            # Last iteration save
            if iteration == self.max_iterations:
                self.save.save_images(iteration=iteration, individual=population[0])
                self.save.save_csv(
                    iteration=iteration,
                    average_mse=stats.compute_average_mse(population),
                    average_fitness=stats.compute_average_fitness(population),
                    best_mse=population[0].mse,
                    best_fitness=population[0].fitness
                )
