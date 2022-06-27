from multiprocessing import Pool, cpu_count

from PIL import Image

from algos.hc import HillClimber
from algos.ppa import Ppa
from algos.sa import SimulatedAnnealing
from utils import Utils

TEST = False

parameters = {
    "canvas_size": None,
    "count_polygons": 0,  # Actual value is computed later
    "max_population_size": 30,
    "count_vertices": 1000,
    "target_image_str": "",
    "save_freq": 1000,
    "max_iterations": 10 ** 6,
    "experiment_name": "First_experiment",
    "target_image": Image
}


def setup() -> None:

    if TEST:
        parameters["experiment_name"] = "Test"
        parameters["max_iterations"] = 1
        parameters["save_frequency"] = 1

    utils = Utils(
        parameters["canvas_size"],
        parameters["target_image_str"],
        parameters["count_vertices"]
    )

    utils.check_directories()

    parameters["count_polygons"] = utils.compute_polygon_count()

    parameters["target_image_str"] = 'img/target/' + parameters["target_image_str"] + '.bmp'


if __name__ == '__main__':
    target_images = ("Starry_Night", "Mona_Lisa", "Mondriaan", "The_Kiss", "Johann_Sebastian_Bach",
                     "The_Persistence_of_Memory", "Convergence")

    count_cpus = cpu_count()
    pool = Pool(processes=count_cpus)

    for target_image in target_images:
        parameters["target_image_str"] = target_image
        setup()

        with Image.open(parameters["target_image_str"]) as img:
            parameters["canvas_size"] = img.size
            parameters["target_image"] = img

            ppa = Ppa(
                **parameters
            )

            hc = HillClimber(
                **parameters
            )

            sa = SimulatedAnnealing(
                **parameters
            )

        pool.apply_async(ppa.run_ppa())
        pool.apply_async(hc.run_hc())
        pool.apply_async(sa.run_sa())

    pool.close()
    pool.join()
