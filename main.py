from PIL import Image

from ppa.ppa import Ppa
from utils import Utils

TEST = True

parameters = {
    "CANVAS_SIZE": (240, 180),
    "COUNT_POLYGONS": 0,  # Actual value is computed later
    "MAX_POPULATION_SIZE": 30,
    "COUNT_VERTICES": 300,
    "TARGET_IMAGE": "Starry_Night",
    "SAVE_FREQUENCY": 10 ** 4,
    "MAX_ITERATIONS": 10 ** 6,
    "EXPERIMENT_NAME": "First_experiment",
}


def setup() -> None:

    if TEST:
        parameters["EXPERIMENT_NAME"] = "Test"
        parameters["MAX_ITERATIONS"] = 100
        parameters["SAVE_FREQUENCY"] = 10

    utils = Utils(
        parameters["CANVAS_SIZE"],
        parameters["TARGET_IMAGE"],
        parameters["COUNT_VERTICES"]
    )

    utils.check_directories()

    utils.validate_target_image()

    parameters["COUNT_POLYGONS"] = utils.compute_polygon_count()

    parameters["TARGET_IMAGE"] = 'img/target/' + parameters["TARGET_IMAGE"] + '.bmp'


if __name__ == '__main__':
    setup()

    with Image.open(parameters["TARGET_IMAGE"]) as img:

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

    ppa.run_ppa()
