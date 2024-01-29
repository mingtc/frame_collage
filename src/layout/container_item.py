import abc
from abc import ABC, abstractmethod
import numpy as ns


class ContainerItem(ABC):
    """
    Abstract Class for items that can be put in a layout container (e.g. images + image frames)
    A ContainerItem is anything that can be put inside a container.
    Since a Container can go inside another Container for more advanced layouts, a Container is also a ContainerItem
    Please see inline documentation for abstract methods.
    """
    # used for boundary sizing calculations where if the content is smaller than the minimum number of pixels,
    # it is meaningless to add it into a container due to the fact that it will be too small to see
    DEFAULT_MINIMUM_CONTENT_WIDTH = 50
    DEFAULT_MINIMUM_CONTENT_HEIGHT = 50

    def __init__(self):
        """
        IMPORTANT: Call super().__init__() in the constructor of any class that inherits from this class
        """

        # numpy array of the image. Note that many Containers do not have an image and it
        # will only generate an image when get_drawable_image() is called in order to save memory
        self._image: ns.ndarray = None

    @abstractmethod
    def get_drawable_image(self) -> ns.ndarray:
        """Used for final output to screen / file where the image is created and/or merged with parent layout"""
        pass

    @abstractmethod
    def get_width(self):
        """Gets the width of the image. For objects with no image, need to keep track of its virtual width/height"""
        pass

    @abstractmethod
    def get_height(self):
        """Gets the height of the image. For objects with no image, need to keep track of its virtual width/height"""
        pass

    @abstractmethod
    def resize_by_width(self, width: int):
        """Resize pictures by imposing a width limit. Height will be adjusted to maintain aspect ratio."""
        pass

    @abstractmethod
    def resize_by_height(self, height: int):
        """Resize pictures by imposing a height limit. Width will be adjusted to maintain aspect ratio."""
        pass

    def resize_to_limit(self, width_limit: int, height_limit: int):
        """Resizes the image to fit within the given width and height limits while maintaining aspect ratio.
        Args:
            width_limit: The maximum allowed width.
            height_limit: The maximum allowed height.
        """

        original_width = self.get_width()
        original_height = self.get_height()
        original_aspect_ratio = original_width / original_height

        # Calculate the width and height the image would have if resized to each limit:
        # This is the width the image would have if its height was resized to height_limit while maintaining the original aspect ratio.
        potential_width_by_height = height_limit * original_aspect_ratio

        # This is the height the image would have if its width was resized to width_limit while maintaining the original aspect ratio.
        potential_height_by_width = width_limit / original_aspect_ratio

        # Choose the resizing method that results in a larger image within both limits:
        if potential_height_by_width > height_limit:
            # Resizing by width would make the height go over the limit
            self.resize_by_height(int(height_limit))
        else:
            # Resizing by height would result in an excessively small width, or would fit correctly
            self.resize_by_width(int(width_limit))

