from random import randint
from typing import Tuple


def generate_vertex(lower_bound: int, upper_bound: int) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    x = randint(lower_bound, upper_bound), randint(lower_bound, upper_bound)
    y = randint(lower_bound, upper_bound), randint(lower_bound, upper_bound)
    return x, y
