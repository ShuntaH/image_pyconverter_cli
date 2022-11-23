import pathlib
from re import Pattern

import pytest

from utils import create_valid_extension_pattern_from, get_image_paths_from_within


def test_create_valid_extension_pattern_from():
    p = create_valid_extension_pattern_from()
    assert type(p) is Pattern
    assert p.pattern == '/*(.jpg|.jpeg|.JPG|.JPEG|.jpe|.jfif|.pjpeg|.pjp|.png|.gif|.tiff|.tif|.webp|.svg|.svgz)$'


def test_get_image_paths_from_within(
        temp_dir_path,
        temp_image_file,
        temp_text_file
):

    _non_existent_dir_path = '/not/exist'
    with pytest.raises(ValueError) as excinfo:
        get_image_paths_from_within(dir_path=_non_existent_dir_path)
    assert f'"{_non_existent_dir_path} does not exists."' == excinfo.value.args[0]

    _empty_dir_path: pathlib.Path = temp_dir_path()
    with pytest.raises(ValueError) as excinfo:
        get_image_paths_from_within(dir_path=_empty_dir_path.__str__())
    assert f'No images within "{_empty_dir_path.__str__()}".' == excinfo.value.args[0]

    _temp_dir_path: pathlib.Path = temp_dir_path()
    valid_ext_image_png = temp_image_file(image_name='valid_ext_png.png', temp_dir_path=_temp_dir_path)
    valid_ext_image_jpg = temp_image_file(image_name='valid_ext_jpg.jpg', temp_dir_path=_temp_dir_path)
    valid_ext_image_jpg2 = temp_image_file(image_name='valid_ext_jpg2.jpg', temp_dir_path=_temp_dir_path)
    invalid_ext_image = temp_text_file(temp_dir_path=_temp_dir_path)

    paths = get_image_paths_from_within(dir_path=_temp_dir_path)

    for p in paths:
        print(p)
    # total count is 3. there is 1 invalid extension file.
    # assert 2 == path_count


