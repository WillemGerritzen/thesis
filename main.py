import os

from PIL import ImageShow, Image

from painting.painting import Painting


def setup() -> None:
    if 'img' not in os.listdir():
        os.mkdir('img')


if __name__ == '__main__':
    setup()

    start_painting = Painting.generate_start_painting()

    with Image.open("img/random_canvas") as img:
        ImageShow.show(img)
