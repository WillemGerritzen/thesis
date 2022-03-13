from typing import List, Tuple


class Polygon(object):
    """ Class containing polygon coordinates and color attribute for simple handling downstream """

    coordinates: List[Tuple[int, int]]
    color: List[int]
