import pathlib
from typing import Callable

import pytest
from PIL import Image


@pytest.fixture(scope='session')
def temp_dest(tmp_path_factory) -> Callable:
    def _temp_dest(dest: str = 'dest'):
        return tmp_path_factory.mktemp(pathlib.Path(dest))

    return _temp_dest


@pytest.fixture(scope='session')
def temp_dir_path(tmp_path_factory) -> Callable:
    def _temp_dir_path(temp: str = 'temp') -> pathlib.Path:
        return tmp_path_factory.mktemp(pathlib.Path(temp))

    return _temp_dir_path


@pytest.fixture(scope="session")
def temp_image_file(tmp_path_factory) -> Callable:
    """
    :param tmp_path_factory: provided by pytest.
    """
    def _temp_image_file(
            image_name: str,
            temp_dir_path: pathlib.Path,
            size: tuple = (320, 240),
            rgb_color: tuple = (0, 128, 255)
    ) -> pathlib.Path:
        """Since the temp_dir_path function returns a new path each time it is called,
        pass the path created, not the function, as the argument."""

        img = Image.new("RGB", size, rgb_color)
        fn = temp_dir_path / image_name
        img.save(fn)
        return fn

    return _temp_image_file
