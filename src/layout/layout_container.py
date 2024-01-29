from typing import List
import numpy as ns
from src.layout.container_item import ContainerItem
from abc import ABC, abstractmethod
from src.layout_exception import LayoutException


# TODO:
# 1. Define LayoutContainer and LayoutLogic relation better. Ideally LayoutLogic should handle all layout details
# and LayoutContainer is the public interface to give / take orders and also perform non-layout related tasks

class LayoutContainer(ContainerItem):
    """ Generic methods for layout that include other Containers and ContainerItems
    IMPORTANT: Do not instantiate this class directly. Use the factory methods in layout_container_factory.py

    It also contains _layout_logic which is an instance of LayoutLogic that governs how items are laid out
    (e.g. horizontal, vertical, grid, etc).
    """

    def __init__(self, width: int, height: int, capacity,
                 padding: tuple, background_color: tuple,
                 item_gutters: tuple, min_content_width: int, min_content_height: int):
        super().__init__()

        # initialize common variables for all layout and assign invalid or default values
        # also serves as a reference of the class variables (please also see parent class)
        # child class implementation should overwrite these values

        # horizontal gutters separate vertical items and is usually included in total height calculations
        self._gutter_horizontal = 0
        # vertical gutters separate horizontal items and is usually included in total width calculations
        self._gutter_vertical = 0
        self._padding_top = 0
        self._padding_right = 0
        self._padding_bottom = 0
        self._padding_left = 0
        self._background_color = (-1, -1, -1)
        self._capacity = -1
        self._width = 0
        self._height = 0
        self._min_content_width = super().DEFAULT_MINIMUM_CONTENT_WIDTH
        self._min_content_height = super().DEFAULT_MINIMUM_CONTENT_HEIGHT
        self._image = None
        self._layout_logic: LayoutLogic = None
        self._items = []

        # set the parameter values if they are supplied. Child classes are encouraged to override in their own
        # constructors.  Some bounds / sanity checking and defaults are set here too.
        if capacity > 0:
            self._capacity = int(capacity)
        else:
            self._capacity = 1
        self._width = int(width)
        self._height = int(height)
        self.set_background_color(background_color)
        self.set_item_gutters(item_gutters)
        self.set_padding(padding)
        if min_content_width > super().DEFAULT_MINIMUM_CONTENT_WIDTH:
            self._min_content_width = min_content_width
        if min_content_height > super().DEFAULT_MINIMUM_CONTENT_HEIGHT:
            self._min_content_height = min_content_height

    def add_item(self, item: ContainerItem):
        """attempts to add an item to the container. Checks for capacity limit and tests whether the container
        has the minimum dimensions to fit the item. See LayoutLogic.check_minimum_dimensions_when_adding_item()
        for more info.

        If all is well, proceed to have all children resize themselves to fit the new item in there
        """
        if self.can_next_item_fit(item):
            self._items.append(item)
            self._layout_logic.resize_items()
        else:
            raise LayoutException("Cannot fit item, try calling can_next_item_fit() first")

    def remove_item(self, item: ContainerItem):
        """
        Removes a specific item from the Container
        If the item is not in the container, it will raise an exception

        :param item: the ContainerItem to remove
        :return:
        """
        self._items.remove(item)
        self._layout_logic.resize_items()

    def can_next_item_fit(self, item: ContainerItem) -> bool:
        """
        tests if the next item will fit by adding it into the container.

        It first checks for capacity limit and then calculates
        whether there is minimum dimensions to fit this new item in
        The item is removed after the test is done.

        :param item: the ContainerItem to check whether it can fit
        :return: True if the item will fit, False otherwise
        """
        if self.get_num_of_items() >= self.get_capacity():
            return False
        else:
            # test appending the items then have the view check its sizes to see if it fits

            # TODO: this adds the actual item onto the _items List itself to
            # facilitate the calculations for layout with respect to its peers.
            # The item is removed afterwards. However, this may cause side effects in the future and
            # is not thread-safe. Try to find a fix without having to add many parameters to many methods
            self._items.append(item)
            try:
                self._layout_logic.check_dimensions_when_adding_item()
            except LayoutException as e:
                return False
            finally:
                self._items.remove(item)
            return True

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def resize_by_width(self, width: int):
        if width == self.get_width():
            return
        # update height by proportion to the difference of old width and new width
        ratio = width / self.get_width()
        self._height = int(self.get_height() * ratio)

        # update width
        self._width = int(width)

        self._layout_logic.resize_items()

    def resize_by_height(self, height: int):
        if height == self.get_height():
            return

        # update width by proportion to the difference of old height and new height
        ratio = height / self.get_height()
        self._width = int(self.get_width() * ratio)

        # update height
        self._height = int(height)
        self._layout_logic.resize_items()

    def get_drawable_image(self) -> ns.ndarray:
        # create a new array of the same size as self._image and fill it with the background color
        image = ns.ones((self.get_height(), self.get_width(), 3), dtype="float32")
        image = image * self._background_color[::-1]
        # draw the image in self._item[0] onto the new array, do this in multiple steps
        # get the image coordinate
        coordinates = self._layout_logic.get_layout_coordinates()
        for item in self._items:
            x_origin, y_origin, x_end, y_end = coordinates.pop(0)
            image[y_origin:y_end, x_origin:x_end] = item.get_drawable_image()
        return image

    def get_num_of_items(self) -> int:
        return len(self._items)

    def get_capacity(self) -> int:
        return self._capacity

    def set_padding(self, padding: tuple = (0, 0, 0, 0)):
        """
        Sets the padding of the container inputted as a tuple. Floats will be converted to int.
        :param padding: (top, right, bottom, left)
        :return:
        """
        if not self.is_padding_valid(padding):
            raise LayoutException("Invalid padding")
        else:
            self._padding_top = int(padding[0])
            self._padding_right = int(padding[1])
            self._padding_bottom = int(padding[2])
            self._padding_left = int(padding[3])

    def get_padding(self) -> (int, int, int, int):
        """
        Gets the padding of the container
        :return: a tuple with the padding in the order of (top, right, bottom, left)
        """
        return self._padding_top, self._padding_right, self._padding_bottom, self._padding_left

    def set_item_gutters(self, item_gutter=(int, int)):
        """
        Space between items in the container inputted as a tuple, Floats will be converted to int.
        :param item_gutter: (horizontal, vertical)
        :return:
        """

        if not self.is_item_gutters_valid(item_gutter):
            raise LayoutException("Invalid item_gutter")

        self._gutter_horizontal = int(item_gutter[0])
        self._gutter_vertical = int(item_gutter[1])

    def get_item_gutters(self) -> (int, int):
        """
        Gets the item gutter of the container
        :return: a tuple with (horizontal gutter, vertical gutter)
        """
        return self._gutter_horizontal, self._gutter_vertical

    def set_background_color(self, background_color: tuple):
        """
        Sets the background color of the container as RGB. Floats will be converted to int.
        :param background_color: tuple with integers for (red, green, blue) from 0-255
        :return:
        """
        if not self.is_background_color_valid(background_color):
            raise LayoutException(f"Invalid background_color")

        self._background_color = background_color

    def get_background_color(self) -> tuple:
        """
        Gets the background color of the container as RGB
        :return: tuple with (R, G, B) from 0-255
        """
        return self._background_color

    def get_items_copy(self) -> [ContainerItem]:
        """
        Returns a copy of the items in the container. This is a shallow copy.
        Items can be modified or asked to modify iteself (e.g. resize) but the actual
        adding / removing of items need to be handled by the container's own add_item / remove_item methods
        :return: a list of ContainerItems
        """
        return self._items.copy()

    def get_current_num_of_items(self) -> int:
        """
        Returns the number of items in the container
        :return: an integer with the number of items in the container
        """
        return len(self._items)

    def get_minimum_content_width(self):
        """
        Gets the minimum allowable width to give to the content to draw. Anything less than this will be
        visually too small and should not be added to the container or used in any meaningful way.

        Content refers to anything inside a LayoutContainer or ContainerItem that is not padding or gutters.
        For example, the actual Image inside the ImageFrame.

        This variable was set on initialization and is not changed after.

        :return: minimum content width
        """
        return self._min_content_width

    def get_minimum_content_height(self):
        """
        Gets the minimum allowable width to give to the content to draw. Anything less than this will be
        visually too small and should not be added to the container or used in any meaningful way.

        Content refers to anything inside a LayoutContainer or ContainerItem that is not padding or gutters.
        For example, the actual Image inside the ImageFrame.

        This variable was set on initialization and is not changed after.

        :return: minimum content height
        """
        return self._min_content_height

    def get_minimum_layout_width(self) -> int:
        """
        This is a delegate to LayoutLogic's version of this method.
        Please refer to LayoutLogic.get_minimum_layout_width() for explanation
        :return: an integer with the minimum layout width
        """

        return self._layout_logic.get_minimum_layout_width()

    def get_minimum_layout_height(self) -> int:
        """
        This is a delegate to LayoutLogic's version of this method.
        Please refer to LayoutLogic.get_minimum_layout_height() for explanation
        :return: an integer with the minimum layout height.
        """
        return self._layout_logic.get_minimum_layout_height()

    def get_max_drawable_width(self) -> int:
        """
        This is a delegate to LayoutLogic's version of this method.
        For real implementation details, refer to LayoutLogic.get_max_content_drawable_width
        or the LayoutLogic's subclass implementation of it.

        :return: an integer with the maximum width that is usable by ALL children combined
        """
        return self._layout_logic.get_max_drawable_width()

    def get_max_drawable_height(self) -> int:
        """This is a delegate to LayoutLogic's version of this method.
        For real implementation details, refer to LayoutLogic.get_max_content_drawable_height
        or the LayoutLogic's subclass implementation of it.

        :return: an integer with the maximum height that is usable by ALL children combined
        """
        return self._layout_logic.get_max_drawable_height()

    def is_padding_valid(self, padding: tuple) -> bool:
        """
        Checks if the padding is valid.
        :param padding: (top, right, bottom, left)
        :return: True if valid, False otherwise
        """
        if padding is None:
            return False
        elif not isinstance(padding, tuple):
            return False
        elif len(padding) != 4:
            return False
        elif not all(isinstance(n, int) and n >= 0 for n in padding):
            return False
        return True

    def is_item_gutters_valid(self, item_gutters: tuple) -> bool:
        """
        Checks if the item_gutters is valid.
        :param item_gutters: (horizontal, vertical)
        :return: True if valid, False otherwise
        """
        if item_gutters is None:
            return False
        elif not isinstance(item_gutters, tuple):
            return False
        elif len(item_gutters) != 2:
            return False
        elif not all(isinstance(n, int) and n >= 0 for n in item_gutters):
            return False
        return True

    def is_background_color_valid(self, background_color: tuple) -> bool:
        """
        Checks if the background_color is valid.
        :param background_color: (red, green, blue)
        :return: True if valid, False otherwise
        """
        if background_color is None:
            return False
        elif not isinstance(background_color, tuple):
            return False
        elif len(background_color) != 3:
            return False
        elif not all(isinstance(n, int) and n >= 0 and n <= 255 for n in background_color):
            return False
        return True


class LayoutLogic(ABC):
    """Abstract class for common functions for each layout logic (e.g. vertical, horizontal, grid, etc)
    Calculations and resizing for this layout will in this class. Methods needed to be callable from
    LayoutContainer should be delegates from LayoutContainer calling into the respective function in
    LayoutLogic.  LayoutLogic should not be used outside its respective LayoutContainer.
    """

    @abstractmethod
    def resize_items(self):
        """
        Iterate through all items in the container and tell each to resize themselves to fit the container
        :return:
        """
        pass

    @abstractmethod
    def get_max_width_for_each_item(self) -> int:
        """
        Calculates the maximum width each item can occupy after taking into account padding / gutters of
        the layout container where the children items do not have access to.
        :return:
        """
        pass

    @abstractmethod
    def get_max_height_for_each_item(self) -> int:
        """
        Calculates the maximum height each item can occupy after taking into account padding / gutters of
        the layout container where the children items do not have access to.
        :return:
        """
        pass

    @abstractmethod
    def get_layout_coordinates(self) -> List:
        """
        Calculates the coordinates of each child item in the container for where to begin / end
        the drawing of each child's image onto the container.
        :return:
        """
        pass

    @abstractmethod
    def check_dimensions_when_adding_item(self):
        """
        # check the width and height of the new item against the cell width and height. If the cell is too small,
        it will not be able to fit and will raise a LayoutException.
        :return:
        """
        # TODO: change it to not raise an exception as original purpose of this method has changed.
        pass

    def get_minimum_layout_height(self) -> int:
        """
        Gets the minimum height that this container can resize itself and its contents to.
        Since it is a container, it also has to ask the items contained within it for
        their minimum_layout_height.

        There is a minimum layout height because of non-resizeable elements such as padding and gutters.
        What is resizeable is the content itself (for example an Image) and other space gaps.
        Content can resize down to minimum content width / height.


        :return: integer with the minimum layout height
        """
        horizontal_gutter, vertical_gutter = self._con.get_item_gutters()
        padding_top, padding_right, padding_bottom, padding_left = self._con.get_padding()

        gutter = horizontal_gutter * max((self._con.get_num_of_items() - 1), 0)
        padding = padding_top + padding_bottom
        minimum_layout_height = gutter + padding
        for item in self._con.get_items_copy():
            if isinstance(item, LayoutContainer):
                minimum_layout_height += item.get_minimum_layout_height()
            elif isinstance(item, ContainerItem):
                minimum_layout_height += self._con.get_minimum_content_height()
        return minimum_layout_height

    def get_minimum_layout_width(self) -> int:
        """
        Gets the minimum height that this container can resize itself and its contents to.
        Since it is a container, it also has to ask the items contained within it for
        their minimum_layout_height.

        There is a minimum layout height because of non-resizeable elements such as padding and gutters.
        What is resizeable is the content itself (for example an Image) and other space gaps.
        Content can resize down to minimum content width / height.


        :return: integer with the minimum layout width.
        """

        horizontal_gutter, vertical_gutter = self._con.get_item_gutters()
        padding_top, padding_right, padding_bottom, padding_left = self._con.get_padding()

        gutter = vertical_gutter * max((self._con.get_num_of_items() - 1), 0)
        padding = padding_left + padding_right
        minimum_layout_width = gutter + padding
        for item in self._con.get_items_copy():
            if isinstance(item, LayoutContainer):
                minimum_layout_width += item.get_minimum_layout_width()
            elif isinstance(item, ContainerItem):
                minimum_layout_width += self._con.get_minimum_content_width()
        return minimum_layout_width

    def get_max_drawable_width(self) -> int:
        """Gets the maximum width that can be used for drawing ALL ContainerItems within this container
        In most cases this is just the width / height minus the padding.

        :return: an integer with the maximum width that is usable by ALL children combined
        """
        padding_top, padding_right, padding_bottom, padding_left = self._con.get_padding()
        return int(self._con.get_width() - padding_left - padding_right)

    def get_max_drawable_height(self) -> int:
        """Gets the maximum height that can be used for drawing ALL ContainerItems within this container
        In most cases this is just the width / height minus the padding.

        :return: an integer with the maximum width that is usable by ALL children combined
        """
        padding_top, padding_right, padding_bottom, padding_left = self._con.get_padding()
        return int(self._con.get_height() - padding_top - padding_bottom)
