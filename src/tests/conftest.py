import pathlib
from typing import Callable

import pytest
from PIL import Image


@pytest.fixture(scope='session')
def temp_dest(tmp_path_factory) -> Callable:
    def _temp_dest_root(dest: str = 'dest'):
        return tmp_path_factory.mktemp(pathlib.Path(dest))

    return _temp_dest_root


@pytest.fixture(scope="session")
def temp_image_file(tmp_path_factory) -> Callable:
    """
    :param tmp_path_factory:
    """
    def _temp_image_file(
            image_name: str,
            size: tuple = (320, 240),
            rgb_color: tuple = (0, 128, 255)
    ):
        img = Image.new("RGB", size, rgb_color)
        fn = tmp_path_factory.mktemp(pathlib.Path('temp')) / image_name
        img.save(fn)
        return fn

    return _temp_image_file
