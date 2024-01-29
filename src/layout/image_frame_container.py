import math
from typing import List

import numpy as ns
from src.layout.container_item import ContainerItem
from src.layout.image import Image
from src.layout.layout_container import LayoutContainer, LayoutLogic


class ImageFrameContainer(LayoutContainer):
    """
        A container class that can only contain one image. While Image can be used without this container, this
        container can add effects to the image such as padding / background color / text on the frame, etc
        """

    def __init__(self, image: Image, padding: tuple, background_color: tuple, min_content_width: int, min_content_height: int):
        """DO NOT DIRECTLY USE THIS CONSTRUCTOR. USE THE FACTORY METHOD INSTEAD in layout_containers_factory.py"""
        super().__init__(1, 1, 1, padding, background_color, (0, 0), min_content_width, min_content_height)
        self._items.append(image)
        self._width = image.get_width() + self._padding_left + self._padding_right
        self._height = image.get_height() + self._padding_top + self._padding_bottom
        self._layout_logic = ImageFrameLayoutLogic(self)

    def get_width(self):
        return int(self._width)

    def get_height(self):
        return int(self._height)

    def resize_by_width(self, width: int):
        # resizing can be somewhat expensive, so we will only resize if the width is different

        if width == self.get_width():
            return

        # calculate ratio of max_width to width
        ratio = width / self.get_width()

        # update width and height of the frame, since nothing is drawn yet, this is easily modifiable
        self._width = int(width);
        # calculate new height by multiplying ratio by height
        self._height = int(self.get_height() * ratio)

        # The image contained inside the frame is drawn already so it needs to be resized.
        # do a sanity check to make sure the image can fit inside the frame
        child_width = int(self.get_max_drawable_width())
        if child_width <= 0:
            raise Exception("The width of the image frame is too small to fit the image.")
        child_height = int(self.get_max_drawable_height())

        # tell image to resize itself
        self._items[0].resize_to_limit(child_width, child_height)

    def resize_by_height(self, height: int):
        if height == self.get_height():
            return

        # calculate ratio of max_height to height
        ratio = height / self.get_height()

        # update width and height of the frame, since nothing is drawn yet, this is easily modifiable
        self._height = int(height)
        # calculate new width by multiplying ratio by width
        self._width = int(self.get_width() * ratio)

        # The image contained inside the frame is drawn already so it needs to be resized.
        # do a sanity check to make sure the image can fit inside the frame
        child_height = int(self.get_max_drawable_height())
        if child_height <= 0:
            raise Exception("The height of the image frame is too small to fit the image.")
        child_width = int(self.get_max_drawable_width())

        # tell image to resize itself
        self._items[0].resize_to_limit(child_width, child_height)

    def add_item(self, item: ContainerItem):
        # will not do anything here because a frame should be initialized with an image already. Consider throwing an
        # exception.
        pass

    def remove_item(self, item: ContainerItem):
        # a frame without an image is incomplete and invites many errors. Consider throwing an exception.
        pass

    # def get_child_origin_coordinates


    def get_drawable_image(self) -> ns.ndarray:
        # create a new array of the same size as self._image and fill it with the background color
        image = ns.ones((self.get_height(), self.get_width(), 3), dtype="float32")
        image = image * self._background_color[::-1]
        # draw the image in self._item[0] onto the new array, do this in multiple steps
        # get the image coordinate
        top_left_coordinate = self._layout_logic.get_layout_coordinates()[0]

        # get the image
        image_to_draw = self._items[0].get_drawable_image()

        # get the height and width of the image
        image_to_draw_width = image_to_draw.shape[1]
        image_to_draw_height = image_to_draw.shape[0]

        bottom_right_coordinate = (
            top_left_coordinate[0] + image_to_draw_width, top_left_coordinate[1] + image_to_draw_height)
        # draw the image onto the new array
        image[top_left_coordinate[1]:bottom_right_coordinate[1],
        top_left_coordinate[0]:bottom_right_coordinate[0]] = image_to_draw
        return image


class ImageFrameLayoutLogic(LayoutLogic):
    def __init__(self, container: ImageFrameContainer):
        self._con = container

    def resize_items(self):
        if len(self._con.get_items_copy()) == 0:
            return
        item = self._con.get_items_copy()[0]
        item.resize_to_limit(self.get_max_width_for_each_item(), self.get_max_height_for_each_item())

    def get_max_width_for_each_item(self) -> int:
        return int(self._con.get_max_drawable_width())

    def get_max_height_for_each_item(self) -> int:
        return int(self._con.get_max_drawable_height())

    def get_layout_coordinates(self) -> List:
        if len(self._con.get_items_copy()) == 0:
            return []
        item = self._con.get_items_copy()[0]

        image_to_draw_width = item.get_width()
        image_to_draw_height = item.get_height()

        padding_top, padding_right, padding_bottom, padding_left = self._con.get_padding()

        x_gap = self._con.get_max_drawable_width() - image_to_draw_width
        x_origin = padding_left + math.floor(int(x_gap / 2))

        y_gap = self._con.get_max_drawable_height() - image_to_draw_height
        y_origin = padding_top + math.floor(int(y_gap / 2))

        coordinates = [(x_origin, y_origin)]

        return coordinates

    def check_dimensions_when_adding_item(self):
        minimum_needed_width = self.get_minimum_layout_width()
        minimum_needed_height = self.get_minimum_layout_height()
        if minimum_needed_width > self._con.get_width() or minimum_needed_height > self._con.get_height():
            raise Exception(
                f"The container is too small to fit the new item.\nMinimum Needed Width: {minimum_needed_width}\nCanvas Width: {self._con.get_width()}\nMinimum Needed Height: {minimum_needed_height}\nCanvas Height: {self._con.get_height()}\n")


