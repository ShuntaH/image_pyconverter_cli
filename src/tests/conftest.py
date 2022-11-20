import pytest
from PIL import Image


@pytest.fixture(scope='session')
def temp_dir():
    return 'temp'


@pytest.fixture(scope="session")
def temp_image_file(
        tmp_path_factory,
        temp_dir
):
    """
    :param request:
    :param temp_dir:
    :param tmp_path_factory:
    :param size: (width, height)
    :param rgb_color: ()
    :return:
    """
    def _temp_image_file(
            image_name: str,
            size: tuple = (320, 240),
            rgb_color: tuple = (0, 128, 255)
    ):
        img = Image.new("RGB", size, rgb_color)
        fn = tmp_path_factory.mktemp(temp_dir) / image_name
        img.save(fn)
        return fn

    return _temp_image_file
