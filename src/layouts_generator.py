import copy
import os
import random
from typing import List

import cv2

import layout_containers_factory
from src.layout import horizontal_container, vertical_container, grid_container
from src.layout.image import Image
from src.layout.layout_container import LayoutContainer

COLORS = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "orange": (255, 165, 0),
    "yellow": (255, 255, 0),
    "green": (0, 128, 0),
    "blue": (0, 0, 255),
    "purple": (128, 0, 128),
    "pink": (255, 192, 203),
    "brown": (165, 42, 42),
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "gray": (128, 128, 128),
    "maroon": (128, 0, 0),
    "olive": (128, 128, 0),
    "teal": (0, 128, 128),
    "navy": (0, 0, 128),
    "aqua": (0, 255, 255),
    "fuchsia": (255, 0, 255),
    "lime": (0, 255, 0),
    "silver": (192, 192, 192),
    "gold": (255, 215, 0)
}

PADDINGS = {
    "none": (0, 0, 0, 0),
    "small": (10, 10, 10, 10),
    "medium": (20, 20, 20, 20),
    "large": (30, 30, 30, 30)
}

GUTTERS = {
    "none": (0, 0),
    "small": (10, 10),
    "medium": (20, 20),
    "large": (30, 30)
}

SCREEN_RESOLUTIONS = {
    "4k": (3840, 2160),
    "1440p": (2560, 1440),
    "1080p": (1920, 1080),
}

SUPPORTED_IMAGE_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png"
}

ASPECT_RATIO_RANGES = {
    "square-ish": (0.751, 1.250),
    "portrait-ish": (1.251, 1.800),
    "landscape-ish": (0.561, 0.750),
    "ultra-wide": (1.801, 3.000),  # anything beyond is too wide to handle, anything beyond will be disregarded
    "ultra-narrow": (0.333, 0.560),  # anything beyond is too narrow to handle, anything beyond will be disregarded
}

HORIZONTAL_LAYOUT_HEURISTICS = {
    # common fields
    "name": "horizontal",
    "minimum_width": 0.25,
    "minimum_height": 0.25,
    "minimum_capacity_for_child_containers": 2,
    "maximum_capacity_for_child_containers": 3,
    "aspect_ratio_preference_order": ["landscape-ish",
                                      "square-ish",
                                      "ultra-wide",
                                      "portrait-ish",
                                      "ultra-narrow"
                                      ],
    # uncommon_fields
    "minimum_capacity": 1,
    "maximum_capacity": 3
}

VERTICAL_LAYOUT_HEURISTICS = {
    # common fields
    "name": "vertical",
    "minimum_width": 0.25,
    "minimum_height": 0.25,
    "minimum_capacity_for_child_containers": 2,
    "maximum_capacity_for_child_containers": 3,
    "aspect_ratio_preference_order": ["portrait-ish",
                                      "square-ish",
                                      "ultra-narrow",
                                      "landscape-ish",
                                      "ultra-wide"
                                      ],
    # uncommon fields
    "minimum_capacity": 1,
    "maximum_capacity": 3,

}

GRID_LAYOUT_HEURISTICS = {
    # common fields
    "name": "grid",
    "minimum_width": 0.3,
    "minimum_height": 0.3,

    "aspect_ratio_preference_order": ["square-ish",
                                      "portrait-ish",
                                      "landscape-ish"
                                      ],
    "minimum_capacity_for_child_containers": 0,
    "maximum_capacity_for_child_containers": 0,

    # uncommon fields
    "minimum_rows": 2,
    "minimum_columns": 2,
    "max_rows": 3,
    "max_columns": 3,
    "minimum_width_per_column": 0.15,
    "minimum_height_per_row": 0.15,
}

LAYOUT_HEURISTICS = {
    "horizontal": HORIZONTAL_LAYOUT_HEURISTICS,
    "vertical": VERTICAL_LAYOUT_HEURISTICS,
    "grid": GRID_LAYOUT_HEURISTICS
}

GENERAL_SETTINGS = {
    "max_levels_to_nest": 2
}


# generates randoom layouts and returns a list of

def run ():
    image_directory = "test_images_3/"
    dict_of_images = create_aspect_ratio_sorted_list_of_images_from_directory(image_directory)
    num_to_generate = 500
    for i in range(num_to_generate):
        file_name_int = random.randint(10000,999999)
        copy_of_dict_of_images = copy.deepcopy(dict_of_images)
        main_container, bottom_level_containers = generate_random_layouts()
        populate_bottom_level_containers(bottom_level_containers, copy_of_dict_of_images)
        cv2.imwrite(f"output/collage_{file_name_int}.jpg", main_container.get_drawable_image())
        print(f"generated image #{i} of {num_to_generate}"  )

def populate_bottom_level_containers(bottom_level_containers : List, dict_of_images: dict):



    for container in bottom_level_containers:
        heuristic_name = None
        if isinstance(container, horizontal_container.HorizontalContainer):
            heuristic_name = LAYOUT_HEURISTICS["horizontal"]["name"]
        elif isinstance(container, vertical_container.VerticalContainer):
            heuristic_name = LAYOUT_HEURISTICS["vertical"]["name"]
        elif isinstance(container, grid_container.GridContainer):
            heuristic_name = LAYOUT_HEURISTICS["grid"]["name"]
        heuristic = LAYOUT_HEURISTICS[heuristic_name]

        for i in range(container.get_capacity()):

            for aspect_ratio_type in heuristic["aspect_ratio_preference_order"]:
                if (len(dict_of_images[aspect_ratio_type]) > 0):
                    image_path = get_random_item_from_list_then_remove(dict_of_images[aspect_ratio_type])
                    image = Image(open_image_file(image_path))
                    image_frame = layout_containers_factory.create_image_frame_container(image, (0, 0, 0, 0), (235, 235, 235))
                    if container.can_next_item_fit(image_frame):
                        container.add_item(image_frame)
                        break
                else:
                    continue
            else:
                break





def generate_random_layouts():
    # generate main layout first, choose biggest canvas first
    random_resolution = "1080p" # random.choice(list(SCREEN_RESOLUTIONS.keys()))
    resolution_width = SCREEN_RESOLUTIONS[random_resolution][0]
    resolution_height = SCREEN_RESOLUTIONS[random_resolution][1]

    random_max_levels_to_nest = random.randint(1, GENERAL_SETTINGS["max_levels_to_nest"])

    # create main container
    random_capacity = random.randint(HORIZONTAL_LAYOUT_HEURISTICS["minimum_capacity"],
                                     HORIZONTAL_LAYOUT_HEURISTICS["maximum_capacity"])
    padding = PADDINGS["small"]
    background_color = COLORS["white"]
    gutters = GUTTERS["small"]
    main_container = layout_containers_factory.create_horizontal_container(resolution_width,
                                                                           resolution_height,
                                                                           random_capacity,
                                                                           padding, background_color, gutters)

    eligible_layouts = [HORIZONTAL_LAYOUT_HEURISTICS]
    bottom_level_containers = generate_random_sub_layouts(main_container, main_container.get_max_drawable_width(),
                                                main_container.get_max_drawable_height(), main_container,
                                                random_max_levels_to_nest, eligible_layouts)

    # add layout to main container
    return main_container, bottom_level_containers


def get_list_of_eligible_layouts(proposed_width, proposed_height, main_container_width, main_container_height):
    eligible_layouts = []
    for layout_heuristic in LAYOUT_HEURISTICS.values():
        if (proposed_width >= main_container_width * layout_heuristic["minimum_width"] and
                proposed_height >= main_container_height * layout_heuristic["minimum_height"]):
            eligible_layouts.append(layout_heuristic)
    return eligible_layouts


def generate_random_sub_layouts(parent_container: LayoutContainer, proposed_width, proposed_height, main_container,
                                nesting_level, eligible_layouts):
    bottom_level_containers = []
    if (len(eligible_layouts) == 0):
        bottom_level_containers.append(parent_container)
        return bottom_level_containers

    random_layout = random.choice(eligible_layouts)
    generated_layout = create_layout_from_type(random_layout, proposed_width, proposed_height)
    if not parent_container.can_next_item_fit(generated_layout):
        bottom_level_containers.append(parent_container)
        return bottom_level_containers

    parent_container.add_item(generated_layout)
    # if adding was somehow not successful (e.g. too full), no need to do the rest

    remaining_nesting_levels = nesting_level - 1

    if remaining_nesting_levels == 0:
        bottom_level_containers.append(generated_layout)
    else:
        random_layout_heuristics = LAYOUT_HEURISTICS[random_layout["name"]]
        random_number_of_child_layouts_to_generate = random.randint(
            random_layout_heuristics["minimum_capacity_for_child_containers"],
            random_layout_heuristics["maximum_capacity_for_child_containers"])
        if random_number_of_child_layouts_to_generate == 0:
            bottom_level_containers.append(generated_layout)
        else:

            eligible_children_layout = generate_random_sub_dimensions(parent_container,
                                                                                random_number_of_child_layouts_to_generate,
                                                                                main_container)

            for children_layout_info in eligible_children_layout:
                child_proposed_width = children_layout_info[0]
                child_proposed_height = children_layout_info[1]
                eligible_layouts = children_layout_info[2]

                generated_bottom_level_containers = generate_random_sub_layouts(generated_layout, child_proposed_width,
                                                                                child_proposed_height, main_container,
                                                                                remaining_nesting_levels,
                                                                                eligible_layouts)
                bottom_level_containers.extend(generated_bottom_level_containers)
    return bottom_level_containers


def create_layout_from_type(layout_type, proposed_width, proposed_height):
    random_padding = PADDINGS["medium"]  # random.choice(list(PADDINGS.keys()))
    random_gutters = GUTTERS["medium"]  # random.choice(list(GUTTERS.keys()))
    random_background_color = COLORS["white"] #COLORS[random.choice(list(COLORS.keys()))]
    random_layout_heuristics = LAYOUT_HEURISTICS[layout_type["name"]]


    generated_layout = None
    if (layout_type == HORIZONTAL_LAYOUT_HEURISTICS):
        random_capacity = random.randint(random_layout_heuristics["minimum_capacity"],
                                         random_layout_heuristics["maximum_capacity"])
        generated_layout = layout_containers_factory.create_horizontal_container(proposed_width, proposed_height,
                                                                                 random_capacity, random_padding,
                                                                                 random_background_color,
                                                                                 random_gutters)
    elif (layout_type == VERTICAL_LAYOUT_HEURISTICS):
        random_capacity = random.randint(random_layout_heuristics["minimum_capacity"],
                                         random_layout_heuristics["maximum_capacity"])
        generated_layout = layout_containers_factory.create_vertical_container(proposed_width, proposed_height,
                                                                               random_capacity, random_padding,
                                                                               random_background_color, random_gutters)
    elif (layout_type == GRID_LAYOUT_HEURISTICS):
        random_rows = random.randint(GRID_LAYOUT_HEURISTICS["minimum_rows"], GRID_LAYOUT_HEURISTICS["max_rows"])
        random_columns = random.randint(GRID_LAYOUT_HEURISTICS["minimum_columns"],
                                        GRID_LAYOUT_HEURISTICS["max_columns"])
        generated_layout = layout_containers_factory.create_grid_container(proposed_width, proposed_height, random_rows,
                                                                           random_columns, random_padding,
                                                                           random_background_color, random_gutters)
    return generated_layout


def generate_random_sub_dimensions(parent_container: LayoutContainer, number_of_children: int,
                                   main_container: LayoutContainer):
    eligible_layout_with_least_unused_space = []
    lowest_unused_space = main_container.get_max_drawable_width() + main_container.get_max_drawable_height()
    for i in range(50):
        eligible_layouts_for_dimensions = generate_eligible_layouts_for_dimensions(parent_container, number_of_children,
                                                                                   main_container)
        unused_space = get_unused_space_for_eligible_layouts(eligible_layouts_for_dimensions,
                                                             parent_container.get_max_drawable_width(),
                                                             parent_container.get_max_drawable_height())
        if unused_space < lowest_unused_space:
            lowest_unused_space = unused_space
            eligible_layout_with_least_unused_space = eligible_layouts_for_dimensions
    return eligible_layout_with_least_unused_space


def generate_eligible_layouts_for_dimensions(parent_container: LayoutContainer, number_of_children: int,
                                             main_container: LayoutContainer):
    parent_width = parent_container.get_max_drawable_width()
    parent_height = parent_container.get_max_drawable_height()

    width_for_each_child = int(parent_width / number_of_children)
    height_for_each_child = int(parent_height / number_of_children)

    width_remaining = parent_width
    height_remaining = parent_height
    children_dimensions = []
    for i in range(number_of_children - 1):
        child_proposed_width = int(random.randint(80, 120) / 100 * width_for_each_child)
        child_proposed_height = int(random.randint(80, 120) / 100 * height_for_each_child)
        children_dimensions.append((child_proposed_width, child_proposed_height))
        width_remaining = width_remaining - child_proposed_width
        height_remaining = height_remaining - child_proposed_height
        children_dimensions.append((child_proposed_width, child_proposed_height))
    child_proposed_width = width_remaining
    child_proposed_height = height_remaining


    eligible_layouts_for_dimensions = []
    main_container_width = main_container.get_max_drawable_width()
    main_container_height = main_container.get_max_drawable_height()
    for dimension in children_dimensions:
        proposed_width = dimension[0]
        proposed_height = dimension[1]
        eligible_layouts = get_list_of_eligible_layouts(proposed_width, proposed_height, main_container_width,
                                                        main_container_height)
        if len(eligible_layouts) > 0:
            eligible_layouts_for_dimensions.append((proposed_width, proposed_height, eligible_layouts))
    return eligible_layouts_for_dimensions


def get_unused_space_for_eligible_layouts(eligible_layouts_for_dimensions: List, parent_width, parent_height):
    total_proposed_width = 0
    total_proposed_height = 0
    for dimension in eligible_layouts_for_dimensions:
        total_proposed_width = total_proposed_width + dimension[0]
        total_proposed_height = total_proposed_height + dimension[1]
    unused_width = parent_width - total_proposed_width
    unused_height = parent_height - total_proposed_height
    return unused_width + unused_height


# open every image in the directory to analyze all of them for aspect ratio
# put them into a dictionary for each aspect ratio.
# to prevent using too much memory at once, open files one by one and only
# save the image path instead of the image.
def create_aspect_ratio_sorted_list_of_images_from_directory(directory: str):
    image_paths = get_list_of_images_from_directory(directory)
    # create aspect_ratio dict with the same keys as ASPECT_RATIO_RANGES
    image_paths_by_aspect_ratio_dict = {}
    for key in ASPECT_RATIO_RANGES.keys():
        image_paths_by_aspect_ratio_dict[key] = []
    # loop through all images and sort them into the aspect_ratio_dict
    for image_path in image_paths:
        image = open_image_file(image_path)
        if image is not None:
            width, height = get_image_width_and_height(image)
            aspect_ratio = get_aspect_ratio(width, height)
            aspect_ratio_key = get_aspect_ratio_dict_key(aspect_ratio)
            if aspect_ratio_key is not None:
                image_paths_by_aspect_ratio_dict[aspect_ratio_key].append(image_path)
    return image_paths_by_aspect_ratio_dict


def get_image_width_and_height(image):
    return image.shape[1], image.shape[0]


def get_aspect_ratio_dict_key(aspect_ratio: int):
    for key, value in ASPECT_RATIO_RANGES.items():
        if aspect_ratio >= value[0] and aspect_ratio <= value[1]:
            return key
    return None


def get_aspect_ratio(width, height):
    return width / height


def get_list_of_images_from_directory(directory: str):
    # create a list of images
    image_paths = []
    # get a list of all image files from folder first. Supported image extensions are in SUPPORTED_IMAGE_EXTENSIONS, file extensions should be case insensitive
    #recurse into subdirectories and do the same
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.split(".")[-1].lower() in SUPPORTED_IMAGE_EXTENSIONS:
                image_paths.append(os.path.join(root, file))


    # for f in os.listdir(directory):
    #     full_path = os.path.join(directory, f)
    #     if os.path.isfile(full_path) and f.split(".")[-1].lower() in SUPPORTED_IMAGE_EXTENSIONS:
    #         image_paths.append(full_path)

    return image_paths
    # loop through all image files


def open_image_file(imagepath: str):
    # not performing checks here since input will be from get_list_ofImages_from_directory()
    img = cv2.imread(imagepath)
    return img


def random_open_x_images(x: int, image_paths: list) -> List:
    images = []
    for i in range(x):
        if (len(image_paths) > 0):
            image = open_image_file(get_random_item_from_list_then_remove(image_paths))
            images.append(image)
    return images


def get_random_item_from_list_then_remove(items: List):
    item = random.choice(items)
    items.remove(item)
    return item
