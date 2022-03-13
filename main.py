import os

from PIL import Image

from ppa.ppa import Ppa
from utils import Utils

parameters = {
    "CANVAS_SIZE": (240, 180),
    "COUNT_POLYGONS": 100,
    "MAX_POPULATION_SIZE": 30,
    "TARGET_IMAGE": "Starry_Night",
    "SAVE_FREQUENCY": 0
}


def setup() -> None:
    if 'img' not in os.listdir():
        os.mkdir('img')
        os.mkdir('img/temp')
        os.mkdir('img/target')

    utils = Utils(parameters["CANVAS_SIZE"], parameters["TARGET_IMAGE"])

    utils.validate_image()

    parameters["TARGET_IMAGE"] = 'img/target/' + parameters["TARGET_IMAGE"] + '.bmp'


if __name__ == '__main__':
    setup()

    with Image.open(parameters["TARGET_IMAGE"]) as img:

        ppa = Ppa(
            img,
            parameters["CANVAS_SIZE"],
            parameters["COUNT_POLYGONS"],
            parameters["MAX_POPULATION_SIZE"],
            parameters["SAVE_FREQUENCY"]
        )

    ppa.run_ppa()





