from random import randint
from typing import Tuple, List

from painting import CANVAS_SIZE

MAX_X, MAX_Y = CANVAS_SIZE[0], CANVAS_SIZE[1]


def generate_coordinates(max_x: int, max_y: int) -> Tuple[int, int]:
    x, y = randint(0, max_x), randint(0, max_y)

    return x, y


def generate_polygon(vertices: int = 3) -> List[Tuple[int, int]]:
    temp_polygon = list(generate_coordinates(MAX_X, MAX_Y))

    for vertex in range(vertices - 1):
        temp_polygon.append(generate_coordinates(MAX_X, MAX_Y))

    polygon = temp_polygon

    return polygon


def generate_polygons(count_polygons: int) -> Tuple[List[Tuple[int, int]], ...]:
    all_polygons = tuple(generate_polygon(vertices=3) for _ in range(count_polygons))
    return all_polygons


def generate_colors(count_polygons: int) -> List[Tuple[int, int, int, int]]:
    color = [(randint(0, 255), randint(0, 255), randint(0, 255), randint(0, 255)) for _ in range(count_polygons)]

    return color
