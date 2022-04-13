from PIL import Image
from multiprocessing import Pool

from ppa.ppa import Ppa
from utils import Utils

TEST = False

parameters = {
    "CANVAS_SIZE": None,
    "COUNT_POLYGONS": 0,  # Actual value is computed later
    "MAX_POPULATION_SIZE": 30,
    "COUNT_VERTICES": 1000,
    "TARGET_IMAGE": "",
    "SAVE_FREQUENCY": 1000,
    "MAX_ITERATIONS": 10 ** 6,
    "EXPERIMENT_NAME": "First_experiment",
}


def setup() -> None:

    if TEST:
        parameters["EXPERIMENT_NAME"] = "Test"
        parameters["MAX_ITERATIONS"] = 1
        parameters["SAVE_FREQUENCY"] = 1

    utils = Utils(
        parameters["CANVAS_SIZE"],
        parameters["TARGET_IMAGE"],
        parameters["COUNT_VERTICES"]
    )

    utils.check_directories()

    parameters["COUNT_POLYGONS"] = utils.compute_polygon_count()

    parameters["TARGET_IMAGE"] = 'img/target/' + parameters["TARGET_IMAGE"] + '.bmp'


if __name__ == '__main__':
    target_images = ("Starry_Night", "Mona_Lisa", "Mondriaan", "The_Kiss", "Johann_Sebastian_Bach",
                     "The_Persistence_of_Memory", "Convergence")
    pool = Pool(processes=64)

    for target_image in target_images:
        parameters["TARGET_IMAGE"] = target_image
        setup()

        with Image.open(parameters["TARGET_IMAGE"]) as img:
            parameters["CANVAS_SIZE"] = img.size

            ppa = Ppa(
                img,
                parameters["CANVAS_SIZE"],
                parameters["COUNT_POLYGONS"],
                parameters["MAX_POPULATION_SIZE"],
                parameters["COUNT_VERTICES"],
                parameters["SAVE_FREQUENCY"],
                parameters["MAX_ITERATIONS"],
                parameters["EXPERIMENT_NAME"]
            )

        pool.apply_async(ppa.run_ppa())

    pool.close()
    pool.join()
