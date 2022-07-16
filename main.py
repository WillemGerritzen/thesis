import importlib
from multiprocessing import Pool, cpu_count

from PIL import Image

from core.utils import Utils

TEST = False

parameters = {
    "canvas_size": None,
    "count_polygons": 0,  # Actual value is computed later
    "max_population_size": 30,
    "count_vertices": 1000,
    "target_image_str": "",
    "save_freq": 1000,
    "max_iterations": 10 ** 6,
    "run_number": "",
    "target_image": Image,
    "algo": ""
}


if __name__ == '__main__':
    utils = Utils(parameters)

    args = utils.parse_arguments()

    parameters["run_number"] = str(args.run)
    parameters["target_image_str"] = args.target_image
    parameters["algo"] = args.algo
    utils.setup()

    count_cpus = cpu_count()
    pool = Pool(processes=count_cpus)

    with Image.open(parameters["target_image_str"]) as img:
        parameters["canvas_size"] = img.size
        parameters["target_image"] = img

    module = importlib.import_module(f"core.algos.{args.algo}")
    algo = getattr(module, args.algo.capitalize())

    algo_to_run = algo(**parameters)
    pool.apply_async(getattr(algo_to_run, "run_" + args.algo)())

    pool.close()
    pool.join()
