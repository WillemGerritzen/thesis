from typing import List, Optional

import numpy as np
from PIL.Image import Image

from models.polygon import Polygon


class Constellation(object):
    """ Constellation model """

    def __init__(self, individual_as_polygons: List[Polygon]):
        self.individual_as_polygons = individual_as_polygons

        self.individual_as_image: Optional[Image] = None
        self.individual_as_array: Optional[np.ndarray] = None

        self.mse: Optional[float] = None
        self.fitness: Optional[float] = None

        self.count_offsprings: Optional[int] = None
        self.count_mutations: Optional[int] = None

    def __add__(self, other):
        return self.fitness + other.fitness

