from typing import Tuple, List

from PIL import ImageDraw, Image


class Draw:
    """ Class taking the empty canvas, the array of polygons and the array of colors to put it all together """

    def __init__(self, canvas: Image, polygons: Tuple[List[Tuple[int, int]], ...],
                 colors: Tuple[Tuple[int, int, int, int], ...]):
        self.canvas = canvas
        self.polygons = polygons
        self.colors = colors

    def draw_polygons(self) -> Image:
        """
        Draws an assortment of randomly generated polygons on a canvas and saves it
        :return: Image object
        """

        draw = ImageDraw.Draw(self.canvas, 'RGBA')

        for polygon_coordinates, color in zip(self.polygons, self.colors):
            draw.polygon(polygon_coordinates, fill=color)  # Draw each polygon and colorize it

        self.canvas.save("img/random_canvas", "bmp")  # Save the resulting canvas

        return self.canvas
