from typing import List, Tuple


class Polygon(object):
    """ Polygon model """

    coordinates: List[Tuple[float, float]]
    color: List[int]

    def __str__(self):
        return f"Coordinates: {self.coordinates}\nColor: {self.color}"
