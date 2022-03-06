from PIL import Image

from painting import CANVAS_SIZE, COUNT_POLYGONS
from painting.canvas import Canvas
from painting.draw import Draw
from painting.polygons import Polygon


class Painting:

    @staticmethod
    def generate_start_painting() -> Image:
        """
        Main script generating the start painting
        :return: The start painting as an Image object
        """
        canvas = Canvas(CANVAS_SIZE)
        empty_canvas = canvas.generate_empty_canvas()

        polygon = Polygon(canvas.size, count_polygons=COUNT_POLYGONS)
        polygons = polygon.generate_polygons()
        colors = polygon.generate_colors()

        assert len(polygons) == len(colors)  # Ensure there are as many polygons as colors

        draw = Draw(empty_canvas, polygons, colors)
        start_painting = draw.draw_polygons()

        return start_painting


