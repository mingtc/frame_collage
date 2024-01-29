from abc import ABC
from typing import List

from src.layout.container_item import ContainerItem
from src.layout.layout_container import LayoutContainer, LayoutLogic
from src.layout_exception import LayoutException


class GridContainer(LayoutContainer):
    def __init__(self, width: int, height: int, rows: int, columns: int,
                 padding: tuple,
                 background_color: tuple,
                 item_gutters: tuple,
                 min_content_width: int,
                 min_content_height: int):
        """DO NOT DIRECTLY USE THIS CONSTRUCTOR. USE THE FACTORY METHOD INSTEAD in layout_containers_factory.py"""
        super().__init__(width, height, rows * columns, padding, background_color,
                         item_gutters, min_content_width, min_content_height)
        self._rows = int(rows)
        self._columns = int(columns)
        self._capacity = int(rows * columns)
        self._layout_logic = GridLayoutLogic(self)

        # initializes cell width / height for grid
        self._layout_logic.resize_items()

        # calculate grid properties

    def get_num_of_rows(self) -> int:
        return self._rows

    def get_num_of_columns(self) -> int:
        return self._columns


class GridLayoutLogic(LayoutLogic):
    def __init__(self, container: GridContainer):
        self._con = container
        self._cell_width = 0
        self._cell_height = 0

    def resize_items(self):
        new_width = self._con.get_width()
        new_height = self._con.get_height()

        horizontal_gutter, vertical_gutter = self._con.get_item_gutters()
        padding_top, padding_right, padding_bottom, padding_left = self._con.get_padding()
        num_of_rows = self._con.get_num_of_rows()
        num_of_cols = self._con.get_num_of_columns()

        # calculate new cell width and height
        self._cell_width = (new_width - padding_left - padding_right - (
                    vertical_gutter * (num_of_cols - 1))) / num_of_cols
        self._cell_width = int(self._cell_width)
        self._cell_height = (new_height - padding_top - padding_bottom - (
                    horizontal_gutter * (num_of_rows - 1))) / num_of_rows
        self._cell_height = int(self._cell_height)

        for item in self._con.get_items_copy():
            item.resize_to_limit(self.get_max_width_for_each_item(), self.get_max_height_for_each_item())

    def get_max_width_for_each_item(self) -> int:
        return self._cell_width

    def get_max_height_for_each_item(self) -> int:
        return self._cell_height

    def get_layout_coordinates(self) -> List:
        # top left corner of each cell in layout
        padding_top, padding_right, padding_bottom, padding_left = self._con.get_padding()
        horizontal_gutter, vertical_gutter = self._con.get_item_gutters()
        x_cell_origin = padding_left
        y_cell_origin = padding_top
        num_of_columns = self._con.get_num_of_columns()
        items_copy = self._con.get_items_copy()
        coordinates = []

        # iterate through items list and fill each cell, from top left to bottom right
        # populate coordinates list with the coordinates of each cell
        current_column_count = 0
        for item in self._con.get_items_copy():
            # calculate the gaps between the cell and the item since the item may not take up the full space of the cell
            x_gap = int((self.get_max_width_for_each_item() - item.get_width()) / 2)
            y_gap = int((self.get_max_height_for_each_item() - item.get_height()) / 2)

            x_content_end = x_cell_origin + x_gap + item.get_width()
            y_content_end = y_cell_origin + y_gap + item.get_height()

            # add exact coordinates to paint into coordinates list after accounting for x_gap
            coordinates.append((x_cell_origin + x_gap, y_cell_origin + y_gap, x_content_end, y_content_end))

            # move x_cell_origin and counter one cell to the right
            x_cell_origin = x_cell_origin + self.get_max_width_for_each_item() + vertical_gutter
            current_column_count += 1

            # if we reached the end of the row, reset x values and increment y values to the next row
            if current_column_count >= num_of_columns:
                current_column_count = 0
                x_cell_origin = padding_left
                y_cell_origin = y_cell_origin + self.get_max_height_for_each_item() + horizontal_gutter

        return coordinates

    def get_minimum_layout_height(self) -> int:
        return self._con.get_height() - self._con.get_minimum_content_height() * self._con.get_num_of_rows()

    def get_minimum_layout_width(self) -> int:
        return self._con.get_width() - self._con.get_minimum_content_width() * self._con.get_num_of_columns()

    def check_dimensions_when_adding_item(self):
        last_item_added: ContainerItem = self._con.get_items_copy()[-1]

        item_to_add_width = last_item_added.get_width()
        item_to_add_height = last_item_added.get_height()

        # if the item is a LayoutContainer, ask what is the smallest it can resize itself to so that
        # it can be asked to resize to fit later.
        if isinstance(last_item_added, LayoutContainer):
            item_to_add_width = last_item_added.get_minimum_layout_width()
            item_to_add_height = last_item_added.get_minimum_layout_height()

        if item_to_add_width > self._cell_width or item_to_add_height > self._cell_height:
            raise LayoutException(
                f"The container or grid cell is too small to fit the new item.\nMaximum height per cell on grid: {self._cell_height}, item height: {item_to_add_height}\nMaximum width per cell on grid: {self._cell_width}, item width: {item_to_add_width}\n")
