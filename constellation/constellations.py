from typing import Tuple

from constellation.canvas import Canvas
from constellation.constellation import Constellation
from constellation.draw import Draw
from constellation.polygons import PolygonGenerator


class Constellations:
    """ Contains methods pertaining to the generation and modification of constellations """

    def __init__(self, canvas_size: Tuple[int, int], count_vertices: int, count_polygons: int, save_freq: bool = 0):
        self.canvas_size = canvas_size
        self.count_polygons = count_polygons
        self.count_vertices = count_vertices
        self.save_freq = save_freq

    def generate_random_polygon_constellation(self) -> Constellation:
        """
        Main script generating a random constellation
        :return: The start constellation as an Image object
        """

        canvas = Canvas(self.canvas_size)
        empty_canvas = canvas.generate_empty_canvas()

        polygon_gen = PolygonGenerator(empty_canvas, self.count_polygons, self.count_vertices)
        constellation = polygon_gen.generate_polygons(initial_vertices=3)

        draw = Draw(empty_canvas, constellation, self.save_freq)
        constellation_as_image = draw.draw_polygons()

        constellation.individual_as_image = constellation_as_image

        return constellation

    def replace_with_mutated_individual(self, mutated_individual: Constellation) -> Constellation:
        """
        Replaces an individual in the population with its mutated counterpart
        :param mutated_individual: The mutated individual
        :return: None
        """

        assert len(mutated_individual.individual_as_polygons) == self.count_polygons  # Make sure the number of polygons hasn't changed during mutation

        # Draw mutated individual
        canvas = Canvas(self.canvas_size)
        empty_canvas = canvas.generate_empty_canvas()

        draw = Draw(empty_canvas, mutated_individual)
        mutated_constellation = draw.draw_polygons()

        mutated_individual.individual_as_image = mutated_constellation

        return mutated_individual



