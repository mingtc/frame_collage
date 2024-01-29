import cv2

import layout_containers_factory
from src.layout.image import Image
import layouts_generator

#create a class that stores screen resolution variables

#screen_1080p_landscape = ScreenProfile(1920, 1080)
#screen_1080p_portrait = ScreenProfile(1080, 1920)
#screen_4k_landscape = ScreenProfile(3840, 2160)
#screen_4k_portrait = ScreenProfile(2160, 3840)

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


#
# Press the green button in the gutter to run the script.
if __name__ == '__main__':


    layouts_generator.run()


#     #tig.create_images_for_colors((200,1000), (300,1200))
#     image_directory = "test_images/"
#     images = ["1.jpg", "2.jpg", "3.jpg", "4.jpg", "5.jpg", "6.jpg"]
#     # Load the images
# #    for i in range(1,20):  # Adjust the number of images as needed
# #        img = cv2.imread(f"{image_directory+str(i)}.jpg")  # Replace with your image paths
# #        image_container = Image(img)
# #        screen_1080p_landscape.add_image_container(image_container)
#
#     #loop 9 times to get 1.jpg ... 9.jpg then open each with cv2.imread and create an image object with it
#
#
#     main_container = layout_containers_factory.create_horizontal_container(1920, 1080, 3, (0, 0, 0, 0), COLORS["white"], (20, 20))
#
#     shared_width = main_container.get_max_drawable_width() / 3
#
#     left_container = layout_containers_factory.create_vertical_container(shared_width, 980, 7, (25, 25, 25, 25),
#                                                                          COLORS["black"], (20, 20))
#     right_container = layout_containers_factory.create_vertical_container(shared_width*2, 980, 7, (25, 25, 25, 25),
#                                                                           COLORS["black"], (20, 20))
#     inner_left_container = layout_containers_factory.create_horizontal_container(shared_width*2-70, 980/2-70, 7, (25, 25, 25, 25),
#                                                                            COLORS["black"], (20, 20))
#
#     inner_right_container = layout_containers_factory.create_grid_container(shared_width*2-70, 980/2-70, 2, 3, (0, 0, 0, 0), COLORS["white"],
#                                                                      (20, 20))
#
#     main_container.add_item(left_container)
#     main_container.add_item(right_container)
#     right_container.add_item(inner_left_container)
#     right_container.add_item(inner_right_container)
#
#
#     for i in range(1,9):
#         img = cv2.imread(f"{image_directory+str(i)}.jpg")
#         image = Image(img)
#         image_frame = layout_containers_factory.create_image_frame_container(image, (0, 0, 0, 0), (235, 235, 235))
#
#         #padding = (random.randint(10,30),random.randint(10,30),random.randint(10,30),random.randint(10,30))
#         #bg_color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
#         #image_frame = layout_containers_factory.create_image_frame_container(image, padding, bg_color)
#
#         if (inner_right_container.can_next_item_fit(image_frame)):
#             inner_right_container.add_item(image_frame)
#         else:
#             break
#
#
#     for i in range(12,19):
#         img = cv2.imread(f"{image_directory+str(i)}.jpg")
#         image = Image(img)
#         image_frame = layout_containers_factory.create_image_frame_container(image, (0, 0, 0, 0), (235, 235, 235))
#
#         #padding = (random.randint(10,30),random.randint(10,30),random.randint(10,30),random.randint(10,30))
#         #bg_color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
#         #image_frame = layout_containers_factory.create_image_frame_container(image, padding, bg_color)
#
#         if (left_container.can_next_item_fit(image_frame)):
#             left_container.add_item(image_frame)
#         else:
#             break
#
#
#     for i in range(6,12):
#         img = cv2.imread(f"{image_directory+str(i)}.jpg")
#         image = Image(img)
#         image_frame = layout_containers_factory.create_image_frame_container(image, (0, 0, 0, 0), (235, 235, 235))
#         # padding = (random.randint(10,30),random.randint(10,30),random.randint(10,30),random.randint(10,30))
#         # bg_color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
#         # image_frame = layout_containers_factory.create_image_frame_container(image, padding, bg_color)
#
#         if inner_left_container.can_next_item_fit(image_frame):
#             inner_left_container.add_item(image_frame)
#         else:
#             break
#
#


    # Save the collage to a file
 #   canvas = screen_1080p_landscape.produce_canvas()
  #  cv2.imwrite("collage.jpg", main_container.get_drawable_image())


