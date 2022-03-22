from typing import List, Optional

from PIL.Image import Image

from constellation.polygon import Polygon


class Constellation(object):
    """ Constellation model """

    def __init__(self, individual_as_polygons: List[Polygon]):
        self.individual_as_polygons = individual_as_polygons

        self.individual_as_image: Optional[Image] = None

        self.mse: Optional[float] = None
        self.fitness: Optional[float] = None

        self.offsprings: Optional[List[Polygon]] = None
        self.count_offsprings: Optional[int] = None
        self.count_mutations: Optional[int] = None

