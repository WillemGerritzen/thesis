import os

from PIL import ImageShow

from painting.painting import Painting


def setup() -> None:
    if 'img' not in os.listdir():
        os.mkdir('img')


if __name__ == '__main__':
    setup()

    start_painting = Painting.generate_start_painting()

    ImageShow.show(start_painting)  # TODO: Figure out how to show with Docker
