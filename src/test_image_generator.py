import numpy as np
import cv2
import os

# declare a dictionary of constants for 20 common colors as RGB tuples with the color name as the key
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

# constant for the default directory to save images in
DEFAULT_DIRECTORY = "test_images_generated/"
DEFAULT_WIDTH_OR_HEIGHT = 300
DEFAULT_FONT_FACE = cv2.FONT_HERSHEY_SIMPLEX


# create a function that loops through the COLORS dictionary and creates an image for each color. It can optionally take in a number range for width and height. If one is supllied, randomly generate each image within that width / height range. If an exact number is supplied, use that for the respective width and height. If no number is supplied, call create_and_save_image without width and height because it has a default anyways. This can also optionally take in a parameter for the directory, if none supplied, use the default one. should save the images with filenames that are numbered from 1 to the length of the COLORS dictionary (e.g. 1.jpg, 2.jpg). Also use the name of the color and save that as text on the image.
def create_images_for_colors(width_range: tuple = None, height_range: tuple = None, directory: str = DEFAULT_DIRECTORY):
    # loop through the COLORS dictionary
    for i, color in enumerate(COLORS):
        # get the width
        width = get_random_number(width_range)
        # get the height
        height = get_random_number(height_range)
        # create the image
        create_and_save_image(width, height, COLORS[color], str(i + 1) + ".jpg", directory, color)


# create a function that takes in a tuple of two numbers and returns a random number between them
def get_random_number(number_range: tuple):
    # if the number range is none, return none
    if number_range is None:
        return DEFAULT_WIDTH_OR_HEIGHT
    # if the number range is a tuple, return a random number between the two numbers
    elif isinstance(number_range, tuple):
        return np.random.randint(number_range[0], number_range[1])
    # if the number range is a number, return that number
    elif isinstance(number_range, int):
        return number_range
    # otherwise return none
    else:
        return DEFAULT_WIDTH_OR_HEIGHT


# create a function that takes in a name, an RGB tuple, a filename, and a directory to save it in, and optional parameters for width and/or height, if none is supplied use 300 x 300)
# take in another parameter to add text to the image, default is empty string in which case no text is added
def create_and_save_image(width, height, color: tuple, filename: str, directory: str, text: str = ""):
    # create the image
    image = create_image(width, height, color, filename)
    # add text to the image, only do this if the string length is greater than 0
    if len(text) > 0:
        image = add_text_to_image(image, text)

    # if directory does not exist, create it
    if not os.path.exists(directory):
        os.makedirs(directory)
    # save the image check for failure and raise an exception since imwrite fails silently if the directory does not exist
    # wrap this in try-catch block
    try:
        cv2.imwrite(directory + filename, image)
    except Exception as e:
        raise Exception("Directory does not exist or error writing to file")


# create a function that takes in parameters to create an image
# based on some parameters: width, height, color as a RGB tuple, a filename. No need to save it yet, just return the ndarray
def create_image(width: int, height: int, color: tuple, filename: str):
    # create a ndarray of 1's with the given width and height
    ones = np.ones((height, width, 3), dtype="uint8")
    # multiply the ndarray by the color tuple, reverse RGB to BGR because opencv takes in BGR instead
    image = ones * color[::-1]
    # return the ndarray
    return image


# add text to the image in a contrasting color, assume the picture is of only of one color when determinine contrast, can just sample any pixel. The size of the text should be no bigger than 50% the width / height of the image.
def add_text_to_image(image: np.ndarray, text: str):
    # get the height and width of the image
    height = image.shape[0]
    width = image.shape[1]
    # get the color of the pixel at 0,0
    color = image[0][0]
    # get the contrast color
    contrast_color = get_contrast_color(color)
    # get the font scale

    # get the font thickness
    font_thickness = get_font_thickness(width, height)
    # get the text size
    text_size, font_scale = get_text_size_and_scale(text, width, DEFAULT_FONT_FACE, font_thickness)
    # get the text coordinates
    text_coordinates = get_text_coordinates(width, height, text_size)
    # add the text to the image
    cv2.putText(image, text, text_coordinates, DEFAULT_FONT_FACE, font_scale, contrast_color, font_thickness,
                cv2.LINE_AA)
    # return the image
    return image


# get the contrast color
def get_contrast_color(color: tuple):
    # get the sum of the color tuple
    color_sum = sum(color)
    # if the sum is less than 382, return white, otherwise return black
    if color_sum < 382:
        return (255, 255, 255)
    else:
        return (0, 0, 0)


# get the font scale based on width and height. The font scale should be no bigger than 50% the width / height of the image.
def get_font_scale(width: int, height: int):
    # get the font scale
    font_scale = min(width, height) / 50
    # return the font scale
    return round(font_scale)


# get the font thickness
def get_font_thickness(width: int, height: int):
    # get the font thickness
    font_thickness = int(min(width, height) / 100)
    # return the font thickness
    return round(font_thickness)


# get the text size
def get_text_size_and_scale(text: str, width: int, fontFace, font_thickness: int) -> (tuple, float):
    # get the text size
    for scale in reversed(range(0, 60, 1)):
        text_size = cv2.getTextSize(text, fontFace, fontScale=scale / 10, thickness=font_thickness)
        new_width = text_size[0][0]
        if new_width <= width:
            return text_size, scale / 10
    return 1


# get the text coordinates
def get_text_coordinates(width: int, height: int, text_size: tuple):
    # get the text width and height
    text_width = text_size[0][0]
    text_height = text_size[0][1]
    # get the text x and y coordinates
    text_x_coordinate = int((width - text_width) / 2)
    text_y_coordinate = int((height + text_height) / 2)
    # return the text coordinates
    return (text_x_coordinate, text_y_coordinate)
