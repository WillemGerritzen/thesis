import os

import cv2

from painting import generate_canvas


def setup() -> None:
    if 'images' not in os.listdir():
        os.mkdir('images')


if __name__ == '__main__':
    setup()
    generate_canvas.generate_empty_canvas()
    generate_canvas.draw_polygons(count_polygons=100)
    img = cv2.imread("images/random_canvas")

    cv2.imshow("random", img)
    cv2.waitKey(0)
