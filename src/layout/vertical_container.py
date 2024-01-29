from typing import List

from src.layout.layout_container import LayoutContainer, LayoutLogic
from src.layout_exception import LayoutException


class VerticalContainer(LayoutContainer):
    def __init__(self, width: int, height: int, capacity: int, padding: tuple, background_color: tuple, item_gutters: tuple,min_content_width: int, min_content_height: int):
        """DO NOT DIRECTLY USE THIS CONSTRUCTOR. USE THE FACTORY METHOD INSTEAD in layout_containers_factory.py"""
        super().__init__(width, height, capacity, padding, background_color,
                         item_gutters, min_content_width, min_content_height)
        self._layout_logic = VerticalLayoutLogic(self)


class VerticalLayoutLogic(LayoutLogic):
    def __init__(self, container: VerticalContainer):
        self._con = container

    def resize_items(self):
        for item in self._con.get_items_copy():
            item.resize_to_limit(self.get_max_width_for_each_item(), self.get_max_height_for_each_item())

    def get_max_width_for_each_item(self) -> int:
        return int(self._con.get_max_drawable_width())

    def get_max_height_for_each_item(self) -> int:
        total_items = self._con.get_current_num_of_items()
        if (total_items == 0):
            return self._con.get_max_drawable_height()
        gutter_horizontal, gutter_vertical = self._con.get_item_gutters()
        max_height_for_each_item = (self._con.get_max_drawable_height() - (
                (total_items - 1) * gutter_horizontal)) / total_items
        return int(max_height_for_each_item)

    def get_layout_coordinates(self) -> List:
        # top left corner of each cell in layout
        padding_top, padding_right, padding_bottom, padding_left = self._con.get_padding()
        x_cell_origin = padding_left
        y_cell_origin = padding_top

        # find maximum width and height we can draw for each child item.
        # current implementation gives each child the same amount of space to write to
        max_width_for_each_item = self.get_max_width_for_each_item()
        max_height_for_each_item = self.get_max_height_for_each_item()

        coordinates = []
        for item in self._con.get_items_copy():
            item_width = item.get_width()
            item_height = item.get_height()

            # gaps are the difference between the max width/height and the item width/height
            x_gap = int(max_width_for_each_item - item_width)
            y_gap = int(max_height_for_each_item - item_height)

            # center the item in the cell
            x_origin = int(x_cell_origin + int(x_gap / 2))
            y_origin = int(y_cell_origin + int(y_gap / 2))

            x_end = int(x_origin + item_width)
            y_end = int(y_origin + item_height)

            coordinates.append((x_origin, y_origin, x_end, y_end))

            # update the y coordinate for the next item
            gutter_horizontal, gutter_vertical = self._con.get_item_gutters()
            y_cell_origin = y_cell_origin + max_height_for_each_item + gutter_horizontal
        return coordinates

    def check_dimensions_when_adding_item(self):
        minimum_needed_height = self.get_minimum_layout_height()
        if minimum_needed_height > self._con.get_height():
            raise LayoutException(
                f"The container is too small to fit the new item.\nMinimum Needed Height: {minimum_needed_height}\nCanvas Height: {self._con.get_height()}\n")
