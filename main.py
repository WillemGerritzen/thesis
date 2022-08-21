import importlib
from multiprocessing import Pool, cpu_count

from PIL import Image

from core.utils import Utils

TEST = False

parameters = {
    "canvas_size": None,
    "count_polygons": 0,  # Actual value is computed later
    "max_population_size": 30,
    "count_vertices": 0,
    "target_image_str": "",
    "save_freq": 1000,
    "max_func_eval": 1000000,
    "run_number": "",
    "target_image": Image,
    "algo": "",
    "max_offspring_count": 5,
    "ffa": False
}


if __name__ == '__main__':
    args = Utils.parse_arguments()

    parameters["run_number"] = str(args.run)
    parameters["target_image_str"] = args.target_image
    parameters["algo"] = args.algo
    parameters['count_vertices'] = args.vertices
    parameters['ffa'] = args.ffa

    utils = Utils(parameters)
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
