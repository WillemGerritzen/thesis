from typing import Tuple, List

from PIL.Image import Image

from constellation.canvas import Canvas
from constellation.draw import Draw
from constellation.polygon import Polygon
from constellation.polygons import PolygonGenerator


class Constellations:
    """ Contains methods pertaining to the generation and modification of constellations """

    def __init__(self, canvas_size: Tuple[int, int], count_polygons: int, save_freq: bool = 0):
        self.canvas_size = canvas_size
        self.count_polygons = count_polygons
        self.save_freq = save_freq

    def generate_random_polygon_constellation(self) -> Tuple[Image, List[Polygon]]:
        """
        Main script generating a random constellation
        :return: The start constellation as an Image object
        """

        canvas = Canvas(self.canvas_size)
        empty_canvas = canvas.generate_empty_canvas()

        polygon_gen = PolygonGenerator(empty_canvas, count_polygons=self.count_polygons)
        polygons = polygon_gen.generate_polygons()

        draw = Draw(empty_canvas, polygons)
        random_polygon_constellation = draw.draw_polygons()

        return random_polygon_constellation, polygons

    def replace_with_mutated_individual(self, mutated_individual: List[Polygon]) -> None:
        """
        Replaces an individual in the population with its mutated counterpart
        :param mutated_individual: The mutated individual
        :return: None
        """

        assert len(mutated_individual) == self.count_polygons

        # Draw mutated individual
        canvas = Canvas(self.canvas_size)
        empty_canvas = canvas.generate_empty_canvas()

        draw = Draw(empty_canvas, mutated_individual)
        mutated_constellation = draw.draw_polygons()
        print(mutated_constellation)



