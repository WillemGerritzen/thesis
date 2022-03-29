from typing import List, Tuple


class Polygon(object):
    """ Polygon model """

    def __init__(self, coordinates : List[Tuple[float, float]], color: List[int]):
        self.coordinates = coordinates
        self.color = color

    def __str__(self):
        return f"Coordinates: {self.coordinates}\nColor: {self.color}"
