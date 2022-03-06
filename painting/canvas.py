import os

from PIL import Image


class Canvas(object):

    def __init__(self, size):
        self.size = size

    def generate_empty_canvas(self) -> Image:
        """
        Generate a white canvas of 240 by 180 pixels in bitmap format
        :return: The empty canvas as an Image object
        """

        if 'empty_canvas' not in os.listdir('img'):
            canvas = Image.new('RGBA', self.size, color=(255, 255, 255, 255))  # 240x180 pixels white canvas
            canvas.save("img/empty_canvas", format="bmp")  # Save in img directory in bitmap format

        else:
            canvas = Image.open('img/empty_canvas')  # If an empty canvas already exists, return it

        return canvas
