import os
from typing import Tuple, Dict, Union

from PIL import Image

from exception_handling import ResizingError


class Utils:

    def __init__(self, parameters: Dict[str, Union[Tuple[int, int], int, str]]):
        self.canvas_size = parameters["CANVAS_SIZE"]
        self.target_image_name = parameters["TARGET_IMAGE"]
        self.target_image = None

        self.count_vertices = parameters["COUNT_VERTICES"]

    def compute_polygon_count(self) -> int:
        """ Computes the number of polygons """

        polygon_count = self.count_vertices // 4

        return polygon_count

    def validate_image(self) -> None:
        """ Validates the target image to ensure it can be used safely """

        self._check_image_existence()
        if not self.target_image:
            raise FileNotFoundError(f"Target image ({self.target_image_name}) not found!")

        self._check_extension()

        if self.target_image.size != self.canvas_size:
            mode = self._determine_mode()

            if mode == 'portrait':
                converted_image = self.target_image.resize((self.canvas_size[1], self.canvas_size[0]))
            elif mode == 'landscape':
                converted_image = self.target_image.resize((self.canvas_size[0], self.canvas_size[1]))
            else:
                raise ResizingError("Something went wrong when resizing the image")

            converted_image.save(self.target_image.filename)

    def _check_image_existence(self) -> None:
        """ Checks the target image can be found and loads it """

        extensions = ['.jpg', '.png', '.bmp']
        for extension in extensions:
            if self.target_image_name + extension in os.listdir('img/target'):
                with Image.open('img/target/' + self.target_image_name + extension) as img:
                    self.target_image = img

    def _determine_mode(self) -> str:
        """
        Checks whether the target image is in portrait or landscape mode
        :return: The target image mode as a string
        """

        if self.target_image.width < self.target_image.height:
            return 'portrait'

        return 'landscape'

    def _check_extension(self) -> None:
        """ Converts the target image to a bitmap file if it is in a different format """

        if not self.target_image.filename.lower().endswith('.bmp'):
            self.target_image.save(self.target_image.filename[:-4] + '.bmp', format="bmp")
            os.remove(self.target_image.filename)
