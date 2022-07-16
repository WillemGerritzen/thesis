from PIL import ImageDraw, Image

from models.constellation import Constellation


class Draw:
    """ Class taking the empty canvas, the array of polygons and the array of colors to put it all together """

    def __init__(self, canvas: Image.Image, polygons: Constellation):
        self.canvas = canvas
        self.polygons = polygons.individual_as_polygons

    def draw_polygons(self) -> Image.Image:
        """
        Draws an assortment of randomly generated polygons on a canvas and optionally, saves it
        :return: Image object
        """

        draw = ImageDraw.Draw(self.canvas, 'RGBA')

        for polygon in self.polygons:
            draw.polygon(polygon.coordinates, fill=tuple(polygon.color))  # Draw each polygon and colorize it

        return self.canvas
