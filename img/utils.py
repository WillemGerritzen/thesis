import os
from typing import Tuple

from PIL import Image


class Utils:

    def __init__(self, canvas_size: Tuple[int, int], target_image_name: str):
        self.canvas_size = canvas_size
        self.target_image_name = target_image_name
        self.target_image = None

    def _check_image_existence(self) -> None:
        extensions = ['.jpg', '.png', '.bmp']
        for extension in extensions:
            if self.target_image_name + extension in os.listdir('img/target'):
                self.target_image = Image.open('img/target/' + self.target_image_name + extension)

    def _determine_mode(self) -> str:
        if self.target_image.width < self.target_image.height:
            return 'portrait'

        return 'landscape'

    def _check_extension(self) -> None:
        if not self.target_image.filename.lower().endswith('.bmp'):
            self.target_image.save(self.target_image.filename[:-4] + '.bmp', format="bmp")
            os.remove(self.target_image.filename)

    def validate_image(self) -> None:

        self._check_image_existence()
        if not self.target_image:
            raise Exception(f"Target image ({self.target_image_name}) not found!")

        mode = self._determine_mode()
        self._check_extension()

        if self.target_image.size != self.canvas_size:
            if mode == 'portrait':
                converted_image = self.target_image.resize((self.canvas_size[1], self.canvas_size[0]))
            elif mode == 'landscape':
                converted_image = self.target_image.resize((self.canvas_size[0], self.canvas_size[1]))
            else:
                raise Exception("Something went wrong when resizing the image")

            converted_image.save(self.target_image.filename)
