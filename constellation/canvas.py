import os

from PIL import Image


class Canvas:

    def __init__(self, size):
        self.size = size

    def generate_empty_canvas(self) -> Image:
        """
        Generate a white canvas of 240 by 180 pixels in bitmap format
        :return: The empty canvas as an Image object
        """

        if 'empty_canvas.bmp' not in os.listdir('img/temp'):
            canvas = Image.new('RGBA', self.size, color=(255, 255, 255, 255))
            canvas.save("img/temp/empty_canvas.bmp", format="bmp")

        else:
            canvas = Image.open('img/temp/empty_canvas.bmp')  # If an empty canvas already exists, return it

        return canvas
