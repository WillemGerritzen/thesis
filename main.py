import argparse
import importlib
from multiprocessing import Pool, cpu_count

from PIL import Image

from utils import Utils

TEST = False
RUNS = 5 if not TEST else 1

parameters = {
    "canvas_size": None,
    "count_polygons": 0,  # Actual value is computed later
    "max_population_size": 30,
    "count_vertices": 1000,
    "target_image_str": "",
    "save_freq": 1000,
    "max_iterations": 10 ** 6,
    "experiment_name": "",
    "target_image": Image
}


def setup() -> None:
    if TEST:
        parameters["experiment_name"] = "Test"
        parameters["max_iterations"] = 1
        parameters["save_freq"] = 1

    utils = Utils(
        parameters["canvas_size"],
        parameters["target_image_str"],
        parameters["count_vertices"]
    )

    utils.check_directories()

    parameters["count_polygons"] = utils.compute_polygon_count()

    parameters["target_image_str"] = 'img/target/' + parameters["target_image_str"] + '.bmp'


if __name__ == '__main__':
    target_images = (
        "Mondriaan",
        "Starry_Night",
        "Mona_Lisa",
        "The_Kiss",
        "Johann_Sebastian_Bach",
        "The_Persistence_of_Memory",
        "Convergence"
    ) if not TEST else ["Mondriaan"]

    parser = argparse.ArgumentParser(description='Approximate paintings with evolutionary algorithms')
    parser.add_argument('algo', type=str, help='Choose the algorithm to run', choices=['hc', 'ppa', 'sa'])
    parser.add_argument('run', type=int, help='Which run this is', choices=range(1, RUNS + 1))
    args = parser.parse_args()

    count_cpus = cpu_count()
    pool = Pool(processes=count_cpus)

    parameters["experiment_name"] = str(args.run)

    for target_image in target_images:
        parameters["target_image_str"] = target_image
        setup()

        with Image.open(parameters["target_image_str"]) as img:
            parameters["canvas_size"] = img.size
            parameters["target_image"] = img

        module = importlib.import_module(f"algos.{args.algo}")
        algo = getattr(module, args.algo.capitalize())

        algo_to_run = algo(**parameters)
        pool.apply_async(getattr(algo_to_run, "run_" + args.algo)())

    pool.close()
    pool.join()
