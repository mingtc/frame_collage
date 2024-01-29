import numpy as ns
import cv2

from src.layout.container_item import ContainerItem

#TODO don't even do resize until an image is required
class Image (ContainerItem):
    # init function to take in an ndarray with type in signature
    def __init__(self, image: ns.ndarray):
        super().__init__()
        self._image = image


    def get_width(self):
        return int(self._image.shape[1])

    def get_height(self):
        return int(self._image.shape[0])

    def resize_by_width(self, width: int):
        int_width = int(width)
        if int_width == self.get_width():
            return

        int_height = int(self.get_height())

        # calculate ratio of max_width to width
        ratio = int_width / self.get_width()
        # calculate new height by multiplying ratio by height
        new_height = int(int_height * ratio)
        # resize image using cv2.resize
        self._image = cv2.resize(self._image, (int_width, new_height))


    def resize_by_height(self, height):
        int_height = int(height)
        if int_height == self.get_height():
            return

        int_width = int(self.get_width())
        # calculate ratio of max_height to height
        ratio = int_height / self.get_height()
        # calculate new width by multiplying ratio by width
        new_width = int(int_width * ratio)
        # resize image using cv2.resize
        self._image = cv2.resize(self._image, (new_width, int_height))

    # get the color of the underlying pixel at the given coordinates
    def get_pixel_color(self, x_coordinate: int, y_coordinate: int):
        return self._image[y_coordinate][x_coordinate]

    # get the canvas
    def get_drawable_image(self) -> ns.ndarray:
        return self._image



