from PIL import ImageDraw, Image

from constellation.constellation import Constellation


class Draw:
    """ Class taking the empty canvas, the array of polygons and the array of colors to put it all together """

    def __init__(self, canvas: Image.Image, polygons: Constellation, save: bool = False, count: int = 0):
        self.canvas = canvas
        self.polygons = polygons.individual_as_polygons
        self.save = save
        self.count = count

    def draw_polygons(self) -> Image.Image:
        """
        Draws an assortment of randomly generated polygons on a canvas and optionally, saves it
        :return: Image object
        """

        draw = ImageDraw.Draw(self.canvas, 'RGBA')

        for polygon in self.polygons:
            draw.polygon(polygon.coordinates, fill=tuple(polygon.color))  # Draw each polygon and colorize it

        if self.save:
            self.canvas.save(f"img/temp/iteration{self.count}.bmp", "bmp")  # Save the resulting canvas

        return self.canvas
