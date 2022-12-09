import pathlib
from typing import Callable, Union

import pytest
from PIL import Image

from src.utils import Stdout, Bcolors, force_cleanup_temp


def pytest_addoption(parser):
    parser.addoption('dir_path', default=pathlib.Path.cwd())


@pytest.fixture(scope='function', autouse=False)
def force_cleanup():
    yield
    force_cleanup_temp()
    Stdout.styled_stdout(Bcolors.OKBLUE.value, 'cleanup done.')


@pytest.fixture(scope='function')
def temp_dest_path(tmp_path) -> Callable:
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
            image_path: Union[str, pathlib.Path],
            temp_dir_path: pathlib.Path,
            size: tuple = (320, 240),
            rgb_color: tuple = (0, 128, 255)
    ) -> pathlib.Path:
        """Since the temp_dir_path function returns a new path each time it is called,
        pass the path created, not the function, as the argument."""

        if type(image_path) is str:
            image_path = pathlib.Path(image_path)

        if image_path.is_absolute():
            raise ValueError(
                '"image_path" should be relative pass because root path is temp_dir_path.')
        parent_image_path = temp_dir_path / image_path.parent
        pathlib.Path.mkdir(parent_image_path, parents=True, exist_ok=True)
        img = Image.new("RGB", size, rgb_color)
        fn = temp_dir_path / image_path
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
