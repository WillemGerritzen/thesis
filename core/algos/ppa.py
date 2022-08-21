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
            max_func_eval: int,
            run_number: str,
            target_image_str: str,
            algo: str,
            max_offspring_count: int,
            ffa: bool
    ) -> None:
        self.canvas_size = canvas_size
        self.count_polygons = count_polygons
        self.max_population_size = max_population_size
        self.count_vertices = count_vertices
        self.target_image = target_image
        self.target_image_array = Utils.bitmap_to_array(self.target_image.filename)
        self.save_freq = save_freq
        self.max_func_eval = max_func_eval
        self.run_number = run_number
        self.target_image_str = target_image_str
        self.algo = algo
        self.max_offspring_count = max_offspring_count
        self.ffa = ffa

        self.constellation = Constellations(self.canvas_size, self.count_vertices, self.count_polygons)
        self.fitness = Fitness(self.target_image_array, self.canvas_size)
        self.mutate = Mutations(self.canvas_size, self.count_polygons, self.count_vertices, self.max_population_size,
                                self.max_offspring_count, self.ffa)
        self.save = SaveResults(self.run_number, self.count_vertices, self.save_freq,
                                os.path.basename(self.target_image.filename)[:-4], self.algo, self.ffa)

    def run_ppa(self) -> Any:
        """ Main PPA logic """
        population = [self.constellation.generate_random_polygon_constellation() for _ in
                      range(self.max_population_size)]

        print(
            f"Run {self.run_number}: Starting {self.algo} with {self.count_vertices} vertices on {self.target_image.filename[7:-4]}")

        offsprings = []
        count_func_eval = len(population)
        base_csv_save = 1
        base_image_save = 1
        mse_dict = {}

        while count_func_eval < self.max_func_eval:
            count_func_eval += len(offsprings)
            population += offsprings
            csv_save = round(count_func_eval, -3)
            image_save = round(count_func_eval, -5)

            # 2. Compute fitness of the whole population
            self.fitness.compute_population_fitness(population)

            for individual in population:
                mse_dict[individual.mse] = 1 if individual.mse not in mse_dict else mse_dict[individual.mse] + 1

            # 3. Sort population and discard the worst individuals
            if self.ffa:
                population = self.fitness.sort_population_by_fitness_frequency(population, mse_dict)[:self.max_population_size]
            else:
                population = self.fitness.sort_population_by_fitness(population)[:self.max_population_size]

            average_fitness = stats.compute_average_fitness(population)
            average_mse = stats.compute_average_mse(population)

            if base_csv_save != csv_save:
                base_csv_save = csv_save
                self.save.save_csv(
                    iteration=count_func_eval,
                    average_mse=average_mse,
                    average_fitness=average_fitness,
                    best_mse=population[0].mse,
                    best_fitness=population[0].fitness
                )

            if base_image_save != image_save:
                base_image_save = image_save
                self.save.save_images(iteration=count_func_eval, individual=population[0])

            # 4. Create offsprings
            offsprings = self.mutate.generate_offsprings(population, mse_dict)

            # Last generation save
            if count_func_eval >= self.max_func_eval:
                self.save.save_images(iteration=count_func_eval, individual=population[0])
                self.save.save_csv(
                    iteration=count_func_eval,
                    average_mse=stats.compute_average_mse(population),
                    average_fitness=stats.compute_average_fitness(population),
                    best_mse=population[0].mse,
                    best_fitness=population[0].fitness
                )
                self.save.save_pickle(mse_dict)
