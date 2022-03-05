import os

from painting import generate_canvas


def setup() -> None:
    if 'images' not in os.listdir():
        os.mkdir('images')


if __name__ == '__main__':
    setup()
    generate_canvas.generate_empty_canvas()
    generate_canvas.draw_polygon()
