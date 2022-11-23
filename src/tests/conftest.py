import pathlib
from typing import Callable

import pytest
from PIL import Image

from src.utils import Stdout, Bcolors


@pytest.fixture(scope='function', autouse=False)
def cleanup():
    yield
    # cleanup_temp()
    Stdout.styled_stdout(Bcolors.OKBLUE.value, 'cleanup done.')


@pytest.fixture(scope='function')
def temp_dest(tmp_path) -> Callable:
    def _temp_dest(dest: str = 'dest'):
        d = tmp_path / pathlib.Path(dest)
        d.mkdir(parents=True, exist_ok=True)
        return d
    yield _temp_dest


@pytest.fixture(scope='function')
def temp_dir_path(tmp_path) -> Callable:
    def _temp_dir(temp: str = 'temp') -> pathlib.Path:
        p = tmp_path / pathlib.Path(temp)
        p.mkdir(parents=True, exist_ok=True)
        return p
    yield _temp_dir


@pytest.fixture(scope='function')
def temp_image_file() -> Callable:
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

    yield _temp_image_file


@pytest.fixture(scope="function")
def temp_text_file() -> Callable:
    def _temp_text_file(
            temp_dir_path: pathlib.Path,
            text_name: str = 'temp.txt',
            content: str = 'content',
    ) -> pathlib.Path:
        """Since the temp_dir_path function returns a new path each time it is called,
        pass the path created, not the function, as the argument."""
        p = temp_dir_path / text_name
        p.write_text(content)
        assert p.read_text() == content
        return p
    yield _temp_text_file
