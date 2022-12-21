# mypy: ignore-errors
import pathlib
from re import Pattern

import pytest

from utils import (
    VALID_EXTENSIONS,
    compile_extension_pattern_from,
    get_image_paths_from_within,
)


def test_create_valid_extension_pattern_from():
    p = compile_extension_pattern_from()
    assert type(p) is Pattern
    assert p.pattern == ".*(.jpg|.jpeg|.JPG|.JPEG|.jpe|.jfif|.pjpeg|.pjp|.png|.gif|.tiff|.tif|.webp|.svg|.svgz)$"


def test_get_image_paths_from_within(
    temp_dir_path,
    temp_image_file,
    temp_text_file,
):
    _non_existent_dir = "/not/exist"
    with pytest.raises(ValueError) as excinfo:
        get_image_paths_from_within(dir_path=_non_existent_dir, valid_extensions=VALID_EXTENSIONS)
    assert f'"{_non_existent_dir} does not exists."' == excinfo.value.args[0]

    _empty_dir_path: pathlib.Path = temp_dir_path()
    with pytest.raises(ValueError) as excinfo:
        get_image_paths_from_within(dir_path=str(_empty_dir_path), valid_extensions=VALID_EXTENSIONS)
    assert f'No images within "{_empty_dir_path}".' == excinfo.value.args[0]

    _temp_dir_path: pathlib.Path = temp_dir_path()
    valid_ext_image_png = temp_image_file(image_path="valid_ext_png.png", temp_dir_path=_temp_dir_path)
    valid_ext_image_jpg = temp_image_file(image_path="valid_ext_jpg.jpg", temp_dir_path=_temp_dir_path)

    paths = get_image_paths_from_within(dir_path=str(_temp_dir_path), valid_extensions=VALID_EXTENSIONS)
    # total count is 3. there is 1 invalid extension file.
    assert 2 == sum(1 for p in paths)

    paths = get_image_paths_from_within(dir_path=str(_temp_dir_path), valid_extensions=VALID_EXTENSIONS)
    for p in paths:
        assert str(p) in [str(valid_ext_image_jpg), str(valid_ext_image_png)]

    # dir_path arg is not a directory
    with pytest.raises(ValueError) as excinfo:
        get_image_paths_from_within(dir_path=valid_ext_image_png, valid_extensions=VALID_EXTENSIONS)
    assert f'"{valid_ext_image_png}" is not a directory. Please specify a directory path.' == excinfo.value.args[0]
