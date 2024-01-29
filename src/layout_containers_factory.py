from src.layout import horizontal_container, vertical_container, image_frame_container, grid_container
from src.layout.container_item import ContainerItem
from src.layout.image import Image


def create_horizontal_container(width: int, height: int, capacity: int = 9,
                                padding: tuple = (0, 0, 0, 0), background_color: tuple = (255, 255, 255),
                                item_gutters: tuple = (0, 0),
                                min_content_width=ContainerItem.DEFAULT_MINIMUM_CONTENT_WIDTH,
                                min_content_height=ContainerItem.DEFAULT_MINIMUM_CONTENT_HEIGHT):
    return horizontal_container.HorizontalContainer(width, height, capacity, padding, background_color, item_gutters,
                                                    min_content_width, min_content_height)


def create_vertical_container(width: int, height: int, capacity: int = 9,
                              padding: tuple = (0, 0, 0, 0), background_color: tuple = (255, 255, 255),
                              item_gutters: tuple = (0, 0),
                              min_content_width=ContainerItem.DEFAULT_MINIMUM_CONTENT_WIDTH,
                              min_content_height=ContainerItem.DEFAULT_MINIMUM_CONTENT_HEIGHT):
    return vertical_container.VerticalContainer(width, height, capacity, padding, background_color, item_gutters,
                                                min_content_width, min_content_height)


def create_image_frame_container(image: Image, padding: tuple = (0, 0, 0, 0),
                                 background_color: tuple = (255, 255, 255),
                                 min_content_width=ContainerItem.DEFAULT_MINIMUM_CONTENT_WIDTH,
                                 min_content_height=ContainerItem.DEFAULT_MINIMUM_CONTENT_HEIGHT):
    return image_frame_container.ImageFrameContainer(image, padding, background_color, min_content_width,
                                                     min_content_height)

def create_grid_container (width: int, height: int, rows: int, columns: int,
                 padding: tuple = (0, 0, 0, 0),
                 background_color: tuple = (255, 255, 255) ,
                 item_gutters: tuple = (0, 0),
                 min_content_width = ContainerItem.DEFAULT_MINIMUM_CONTENT_WIDTH,
                 min_content_height = ContainerItem.DEFAULT_MINIMUM_CONTENT_HEIGHT
                           ):
    return grid_container.GridContainer(width, height, rows, columns, padding, background_color, item_gutters, min_content_width, min_content_height)