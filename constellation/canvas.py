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

        canvas = Image.new('RGB', self.size, color=(0, 0, 0))

        return canvas
