from typing import Tuple, List

from PIL import Image

from constellation.constellation import Constellation
from .mean_squared_error import MSE
from .utils import utils


class Ppa:
    """
    1. Generate random population of polygon constellations (Size = M = 30)
    2. Compute MSE
    3. Sort population (keeping best M individuals)
    4. Create offsprings (each individual creates nr new individuals)
    5. Back to step 2.
    """

    def __init__(self, canvas_size: Tuple[int, int], count_polygons: int, max_population_size: int, target_image: Image):
        self.canvas_size = canvas_size
        self.count_polygons = count_polygons
        self.max_population_size = max_population_size
        self.target_image = target_image

    def generate_population(self) -> List:
        """
        1. Generate random population of polygon constellations
        :return:
        """
        constellation = Constellation(self.canvas_size, self.count_polygons)

        initial_random_constellations = [constellation.generate_random_polygon_constellation() for _ in
                                         range(self.max_population_size)]

        return initial_random_constellations

    def run_ppa(self):
        """
        TBD
        :return: None
        """
        target_image_array = utils.bitmap_to_array(self.target_image.filename)
        mse = MSE(target_image_array)

        all_individuals = self.generate_population()

        # 2. Compute MSE
        mse = mse.compute_mean_squared_error(utils.bitmap_to_array(all_individuals[0].filename))
        print(mse)


