########
# test #
########
from PIL import Image


def make_new_temp_image(
        image_name,
        size: tuple = (320, 240),
        rgb_color: tuple = (0, 128, 255),
):
    """

    :param image_name: add also image extension.
    :param size: (width, height)
    :param rgb_color: ()
    :return:
    """
    image_path = f'{TEST_IMAGE_DIR_PATH}/{image_name}'
    img = Image.new("RGB", size, rgb_color)
    img.save(image_path, quality=95)
