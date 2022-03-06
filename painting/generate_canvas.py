import os

from PIL import Image, ImageDraw

from painting import CANVAS_SIZE
from painting.generate_polygons import generate_polygons, generate_colors


def generate_empty_canvas() -> None:
    """ Generate a white canvas of 240 by 180 pixels in bitmap format """

    if 'empty_canvas' not in os.listdir('images'):
        canvas = Image.new("RGB", CANVAS_SIZE, (255, 255, 255))  # 240x180 pixels white canvas

        canvas.save("images/empty_canvas", format="bmp")  # Save in images directory in bitmap format


def draw_polygons(count_polygons: int = 100) -> None:
    all_polygons = generate_polygons(count_polygons)
    colors = generate_colors(count_polygons)

    assert len(all_polygons) == len(colors)

    with Image.open("images/empty_canvas") as im:
        draw = ImageDraw.Draw(im)
        for polygon_coordinates, color in zip(all_polygons, colors):
            draw.polygon(polygon_coordinates, fill=color)
        im.save("images/random_canvas", "bmp")
