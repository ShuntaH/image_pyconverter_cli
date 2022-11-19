import pytest
from PIL import Image


@pytest.fixture(scope="session")
def temp_image_file(
        tmp_path_factory,
        image_name,
        size: tuple = (320, 240),
        rgb_color: tuple = (0, 128, 255),
):
    """
    :param tmp_path_factory:
    :param image_name: add also image extension.
    :param size: (width, height)
    :param rgb_color: ()
    :return:
    """
    img = Image.new("RGB", size, rgb_color)
    fn = tmp_path_factory.mktemp("temp") / image_name
    img.save(fn)
    return fn
