from typing import Tuple

from PIL import Image

from constellation.canvas import Canvas
from constellation.draw import Draw
from constellation.polygons import Polygon


class Constellation:
    all_constellations_info = {
        "polygon_coordinates": [],
        "polygon_colors": []
    }

    def __init__(self, canvas_size: Tuple[int, int], count_polygons: int):
        self.canvas_size = canvas_size
        self.count_polygons = count_polygons

    def generate_random_polygon_constellation(self) -> Image:
        """
        Main script generating a random constellation
        :return: The start constellation as an Image object
        """
        canvas = Canvas(self.canvas_size)
        empty_canvas = canvas.generate_empty_canvas()

        polygon = Polygon(canvas, count_polygons=self.count_polygons)

        polygon_coordinates = polygon.generate_polygons()
        polygon_colors = polygon.generate_colors()

        assert len(polygon_coordinates) == len(polygon_colors), "Not the same number of polygons and colors"  # Ensure there are as many polygons as colors

        Constellation.all_constellations_info["polygon_coordinates"].append(polygon_coordinates)
        Constellation.all_constellations_info["polygon_colors"].append(polygon_colors)

        draw = Draw(empty_canvas, polygon_coordinates, polygon_colors)
        random_polygon_constellation = draw.draw_polygons()

        return random_polygon_constellation
