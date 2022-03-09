import os

from PIL import Image

from img.utils import Utils
from ppa.ppa import Ppa

parameters = {
    "CANVAS_SIZE": (240, 180),
    "COUNT_POLYGONS": 100,
    "MAX_POPULATION_SIZE": 30,
    "TARGET_IMAGE": "Starry_Night"
}


def setup() -> None:
    if 'img' not in os.listdir():
        os.mkdir('img')

    utils = Utils(parameters["CANVAS_SIZE"], parameters["TARGET_IMAGE"])

    utils.validate_image()

    parameters["TARGET_IMAGE"] = 'img/target/' + parameters["TARGET_IMAGE"] + '.bmp'


if __name__ == '__main__':
    setup()

    ppa = Ppa(
        parameters["CANVAS_SIZE"],
        parameters["COUNT_POLYGONS"],
        parameters["MAX_POPULATION_SIZE"],
        Image.open(parameters["TARGET_IMAGE"])
    )

    ppa.run_ppa()





