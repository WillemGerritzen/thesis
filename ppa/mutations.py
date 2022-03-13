import random
from typing import List

from constellation.polygon import Polygon


class Mutations:
    """ Contains all the functions pertaining to the mutation section of the PPA """

    def __init__(self, count_polygons: int):
        self.count_polygons = count_polygons

    def change_drawing_index(self, polygons: List[Polygon]) -> List[Polygon]:
        """
        Randomly selects a Polygon and assigns it a new randomly selected drawing order
        :param polygons: A list containing the Polygon objects in a constellation
        :return: A list of Polygon objects with the modified Polygon
        """

        chosen_polygon = random.choice(polygons)
        new_idx = random.randint(0, self.count_polygons)

        polygons.remove(chosen_polygon)
        polygons.insert(new_idx, chosen_polygon)

        return polygons

    @staticmethod
    def change_color(polygons: List[Polygon]) -> List[Polygon]:
        """
        Randomly selects a polygon, an RGBA-channel and a new color, and switches the channel to that new color
        :param polygons: A list containing the Polygon objects in a constellation
        :return: A list of Polygon objects with the modified Polygon
        """
        chosen_polygon = random.choice(polygons)
        chosen_channel = random.randint(0, 3)
        random_new_color = random.randint(0, 255)

        chosen_polygon.color[chosen_channel] = random_new_color

        return polygons
