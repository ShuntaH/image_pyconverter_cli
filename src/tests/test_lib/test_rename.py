# mypy: ignore-errors
import dataclasses
import pathlib
import re
from typing import List, Union

import pytest

from lib.rename import DefaultValues, Rename, RenameArgsValidator
from utils import datetime2str, get_dest_dir_name, is_os_windows


@pytest.fixture(scope="function")
def rename_class_mock(temp_dest_path, temp_dir_path) -> Rename:
    @dataclasses.dataclass
    class RenameMock(Rename):
        dir_path: pathlib.Path = temp_dir_path()
        now_str: str = datetime2str()
        dest: Union[str, pathlib.Path] = temp_dest_path()
        loop_count: int = 1

    yield RenameMock


class TestRenameArgsValidator:
    # todo make arg mock

    @dataclasses.dataclass
    class ArgMock:
        new_name: str

    def test_validate_new_name(self, temp_image_file, rename_class_mock):
        # new_name contains file extension characters.
        _new_name_with_ext = "new.png"
        args = self.ArgMock(new_name=_new_name_with_ext)
        validator = RenameArgsValidator(args=args)
        with pytest.raises(ValueError) as excinfo:
            validator.validate_new_name()
        assert excinfo.value.args[0] == f'--new_name option "{_new_name_with_ext}" contains extension characters.'


class TestRename:
    def test_post_init(self, temp_image_file, rename_class_mock):
        _temp_dir: pathlib.Path = rename_class_mock.dir_path
        _temp_dest: pathlib.Path = rename_class_mock.dest
        _temp_image_file: pathlib.Path = temp_image_file(image_path="post_init_test.vol1.png", temp_dir_path=_temp_dir)

        rename = rename_class_mock(image_path=_temp_image_file)

        assert rename.dir_path == _temp_dir
        assert rename.relative_dir_path == _temp_dir.relative_to(_temp_dir)
        assert rename.relative_image_path == _temp_image_file.relative_to(_temp_dir)
        assert rename.relative_image_parent_path == rename.relative_image_path.parents[0]
        assert rename.original_image_name == _temp_image_file.name
        assert rename.ext == ".png"
        assert rename.original_image_stem == "post_init_test.vol1"
        assert rename.renamed_image_stem == "post_init_test.vol1"
        assert rename.zero_padding_string == "{{0:0{}d}}".format(rename.zero_padding_digit)
        assert type(rename.replacement_with_separator_pattern) is re.Pattern
        assert rename.dest == _temp_dest
        assert rename.dest_dir_name == get_dest_dir_name(dir_path=_temp_dir, now_str=rename.now_str)
        assert rename.dest_dir_path == _temp_dest / rename.dest_dir_name
        assert rename.dest_dir_path.exists() is True

    def test_replace_all(self, temp_image_file, rename_class_mock):
        _temp_dir: pathlib.Path = rename_class_mock.dir_path
        _original_path = "original.png"
        _temp_image_file: pathlib.Path = temp_image_file(image_path=_original_path, temp_dir_path=_temp_dir)
        _new_name = "new"

        # missing is_all_replaced_with_new_name and new_name
        rename = rename_class_mock(image_path=_temp_image_file)
        assert hasattr(rename.__class__, "is_all_replaced_with_new_name") is True
        assert hasattr(rename, "is_all_replaced_with_new_name") is True
        assert rename.is_all_replaced_with_new_name is False
        assert hasattr(rename.__class__, "new_name") is True
        assert hasattr(rename, "new_name") is True
        assert rename.new_name == DefaultValues.NEW_NAME.value
        rename.replace_all()
        assert rename.renamed_image_name == _original_path  # not change

        # missing is_all_replaced_with_new_name but new name option is passed.
        rename = rename_class_mock(image_path=_temp_image_file, new_name=_new_name)
        rename.replace_all()
        assert rename.renamed_image_name == _original_path  # not change

        # missing new_name but is_all_replaced_with_new_name is True
        rename = rename_class_mock(image_path=_temp_image_file, is_all_replaced_with_new_name=True)
        with pytest.raises(ValueError) as excinfo:
            rename.replace_all()
        assert excinfo.value.args[0] == "Specify a new name of the image. (e.g. --new_name newname)"

        rename = rename_class_mock(image_path=_temp_image_file, is_all_replaced_with_new_name=True, new_name=_new_name)
        rename.replace_all()
        assert rename.renamed_image_stem == _new_name
        assert _new_name != _original_path

    def test_replace_words(self, temp_image_file, rename_class_mock):
        _temp_dir: pathlib.Path = rename_class_mock.dir_path
        _before = "bar_foo_fuga.png"
        _temp_image_file: pathlib.Path = temp_image_file(image_path=_before, temp_dir_path=_temp_dir)
        _after = "replaced-bar_replaced-foo_replaced-fuga.png"
        chars_before_replacement: List[str] = ["bar", "foo", "fuga"]
        chars_after_replacement: List[str] = ["replaced-bar", "replaced-foo", "replaced-fuga"]

        # missing chars_before_replacement and chars_after_replacement
        rename = rename_class_mock(image_path=_temp_image_file)
        assert hasattr(rename.__class__, "chars_before_replacement") is False
        assert hasattr(rename, "chars_before_replacement") is True
        assert type(rename.chars_before_replacement) is list
        assert len(rename.chars_before_replacement) == 0
        assert hasattr(rename.__class__, "chars_after_replacement") is False
        assert hasattr(rename, "chars_after_replacement") is True
        assert type(rename.chars_after_replacement) is list
        assert len(rename.chars_after_replacement) == 0
        rename.replace_words()
        assert rename.renamed_image_name == _before  # not change

        # missing chars_after_replacement
        rename = rename_class_mock(image_path=_temp_image_file, chars_before_replacement=chars_before_replacement)
        rename.replace_words()
        assert rename.renamed_image_name == _before  # not change

        # missing chars_before_replacement
        rename = rename_class_mock(image_path=_temp_image_file, chars_after_replacement=chars_after_replacement)
        rename.replace_words()
        assert rename.renamed_image_name == _before  # not change

        rename = rename_class_mock(
            image_path=_temp_image_file,
            chars_before_replacement=chars_before_replacement,
            chars_after_replacement=chars_after_replacement,
        )
        rename.replace_words()
        assert rename.renamed_image_name == _after

        # short of chars_before_replacement
        _after = "replaced-bar_foo_fuga.png"
        chars_before_replacement: List[str] = ["bar"]
        chars_after_replacement: List[str] = ["replaced-bar", "replaced-foo", "replaced-fuga"]
        rename = rename_class_mock(
            image_path=_temp_image_file,
            chars_before_replacement=chars_before_replacement,
            chars_after_replacement=chars_after_replacement,
        )
        rename.replace_words()
        assert rename.renamed_image_name == _after

        # short of chars_after_replacement
        _after = "replaced-bar_foo_fuga.png"
        chars_before_replacement: List[str] = ["bar", "foo", "fuga"]
        chars_after_replacement: List[str] = ["replaced-bar"]
        rename = rename_class_mock(
            image_path=_temp_image_file,
            chars_before_replacement=chars_before_replacement,
            chars_after_replacement=chars_after_replacement,
        )
        rename.replace_words()
        assert rename.renamed_image_name == _after

        # chars_before_replacement is empty
        chars_before_replacement: List[str] = list()
        chars_after_replacement: List[str] = ["replaced-bar"]
        rename = rename_class_mock(
            image_path=_temp_image_file,
            chars_before_replacement=chars_before_replacement,
            chars_after_replacement=chars_after_replacement,
        )
        rename.replace_words()
        assert rename.renamed_image_name == _before

        # chars_after_replacement is empty
        chars_before_replacement: List[str] = ["bar", "foo"]
        chars_after_replacement: List[str] = list()
        rename = rename_class_mock(
            image_path=_temp_image_file,
            chars_before_replacement=chars_before_replacement,
            chars_after_replacement=chars_after_replacement,
        )
        rename.replace_words()
        assert rename.renamed_image_name == _before

    def test_replace_full_width_characters_with_half_width(self, temp_image_file, rename_class_mock):
        """
        name００１.png => name001.png
        """
        _temp_dir: pathlib.Path = rename_class_mock.dir_path

        # half-width ASCII characters don't change.
        _before = "half_width.png"
        _temp_image_file: pathlib.Path = temp_image_file(image_path=_before, temp_dir_path=_temp_dir)

        rename = rename_class_mock(image_path=_temp_image_file)
        rename.zen2han()
        assert rename.renamed_image_name == _before

        # full-width ASCII characters to half-width
        _before = "ｆｕｌｌｗｉｄｔｈ.png"
        _after = "fullwidth.png"
        _temp_image_file: pathlib.Path = temp_image_file(image_path=_before, temp_dir_path=_temp_dir)

        rename = rename_class_mock(image_path=_temp_image_file)
        rename.zen2han()
        assert rename.renamed_image_name == _after

        # Non-ASCII characters are not converted to half-width characters.
        _before = "全角.png"
        _temp_image_file: pathlib.Path = temp_image_file(image_path=_before, temp_dir_path=_temp_dir)

        rename = rename_class_mock(image_path=_temp_image_file)
        rename.zen2han()
        assert rename.renamed_image_name == _before

        # half-width numbers don't change.
        _before = "123.png"
        _temp_image_file: pathlib.Path = temp_image_file(image_path=_before, temp_dir_path=_temp_dir)

        rename = rename_class_mock(image_path=_temp_image_file)
        rename.zen2han()
        assert rename.renamed_image_name == _before

        # full-width numbers to half-width
        _before = "１２３.png"
        _after = "123.png"
        _temp_image_file: pathlib.Path = temp_image_file(image_path=_before, temp_dir_path=_temp_dir)

        rename = rename_class_mock(image_path=_temp_image_file)
        rename.zen2han()
        assert rename.renamed_image_name == _after

        # full width space to half width space.
        _before = "ｓｐａｃｅ　ｓｐａｃｅ.png"
        _after = "space space.png"
        _temp_image_file: pathlib.Path = temp_image_file(image_path=_before, temp_dir_path=_temp_dir)

        rename = rename_class_mock(image_path=_temp_image_file)
        rename.zen2han()
        assert rename.renamed_image_name == _after

    def test_replace_delimiters_and_separators_with_specified_separator(self, temp_image_file, rename_class_mock):
        _temp_dir: pathlib.Path = rename_class_mock.dir_path

        # missing is_separator_and_delimiter_replaced
        # replacement_with_separator_pattern
        # separator
        _before = "space space.png"
        _after = "space_space.png"
        _temp_image_file: pathlib.Path = temp_image_file(image_path=_before, temp_dir_path=_temp_dir)
        rename = rename_class_mock(image_path=_temp_image_file)
        assert rename.is_separator_and_delimiter_replaced is False
        assert (
            rename.replacement_with_separator_pattern.pattern
            == re.compile(DefaultValues.REPLACEMENT_WITH_SEPARATOR_PATTERN.value).pattern
        )
        assert rename.separator == DefaultValues.SEPARATOR.value
        rename.replace_with_separator()
        assert rename.renamed_image_name == _before

        # replace half width space with a separator
        _before = "space space.png"
        _after = "space_space.png"
        _temp_image_file: pathlib.Path = temp_image_file(image_path=_before, temp_dir_path=_temp_dir)
        rename = rename_class_mock(image_path=_temp_image_file, is_separator_and_delimiter_replaced=True)
        rename.replace_with_separator()
        assert rename.renamed_image_name == _after

        # replace full width space with a separator
        _before = "space　space.png"
        _after = "space_space.png"
        _temp_image_file: pathlib.Path = temp_image_file(image_path=_before, temp_dir_path=_temp_dir)
        rename = rename_class_mock(image_path=_temp_image_file, is_separator_and_delimiter_replaced=True)
        rename.replace_with_separator()
        assert rename.renamed_image_name == _after

        # replace tab space with a separator
        _before = "space    space.png"
        _after = "space____space.png"
        _temp_image_file: pathlib.Path = temp_image_file(image_path=_before, temp_dir_path=_temp_dir)
        rename = rename_class_mock(image_path=_temp_image_file, is_separator_and_delimiter_replaced=True)
        rename.replace_with_separator()
        assert rename.renamed_image_name == _after

        # replace '.' with a separator
        # '.' looks some file extension.
        _before = "space.space.png"
        _after = "space_space.png"
        _temp_image_file: pathlib.Path = temp_image_file(image_path=_before, temp_dir_path=_temp_dir)
        rename = rename_class_mock(image_path=_temp_image_file, is_separator_and_delimiter_replaced=True)
        rename.replace_with_separator()
        assert rename.renamed_image_name == _after

        # replace ',' with a separator
        _before = "space,space.png"
        _after = "space_space.png"
        _temp_image_file: pathlib.Path = temp_image_file(image_path=_before, temp_dir_path=_temp_dir)
        rename = rename_class_mock(image_path=_temp_image_file, is_separator_and_delimiter_replaced=True)
        rename.replace_with_separator()
        assert rename.renamed_image_name == _after

        # replace '-' with a separator
        _before = "space-space.png"
        _after = "space_space.png"
        _temp_image_file: pathlib.Path = temp_image_file(image_path=_before, temp_dir_path=_temp_dir)
        rename = rename_class_mock(image_path=_temp_image_file, is_separator_and_delimiter_replaced=True)
        rename.replace_with_separator()
        assert rename.renamed_image_name == _after

        # replace 'ー' with a separator
        _before = "spaceーspace.png"
        _after = "space_space.png"
        _temp_image_file: pathlib.Path = temp_image_file(image_path=_before, temp_dir_path=_temp_dir)
        rename = rename_class_mock(image_path=_temp_image_file, is_separator_and_delimiter_replaced=True)
        rename.replace_with_separator()
        assert rename.renamed_image_name == _after

        # replace '_' with not a default separator
        _before = "space_space.png"
        _after = "space-space.png"
        _temp_image_file: pathlib.Path = temp_image_file(image_path=_before, temp_dir_path=_temp_dir)
        rename = rename_class_mock(image_path=_temp_image_file, separator="-", is_separator_and_delimiter_replaced=True)
        rename.replace_with_separator()
        assert rename.renamed_image_name == _after

    def test_add_prefix_and_suffix(self, temp_image_file, rename_class_mock):
        _temp_dir: pathlib.Path = rename_class_mock.dir_path

        # missing prefix and suffix
        _before = "image.png"
        _after = "image.png"
        _temp_image_file: pathlib.Path = temp_image_file(image_path=_before, temp_dir_path=_temp_dir)
        rename = rename_class_mock(image_path=_temp_image_file)
        rename.add_prefix_suffix()
        assert rename.renamed_image_name == _before
        assert _before == _after

        # add prefix
        _before = "image.png"
        _after = "prefix_image.png"
        _temp_image_file: pathlib.Path = temp_image_file(image_path=_before, temp_dir_path=_temp_dir)

        rename = rename_class_mock(image_path=_temp_image_file, prefix="prefix")
        rename.add_prefix_suffix()
        assert rename.renamed_image_name == _after

        # add suffix
        _before = "image.png"
        _after = "image_suffix.png"
        _temp_image_file: pathlib.Path = temp_image_file(image_path=_before, temp_dir_path=_temp_dir)

        rename = rename_class_mock(image_path=_temp_image_file, suffix="suffix")
        rename.add_prefix_suffix()
        assert rename.renamed_image_name == _after

        # add both prefix and suffix
        _before = "image.png"
        _after = "prefix_image_suffix.png"
        _temp_image_file: pathlib.Path = temp_image_file(image_path=_before, temp_dir_path=_temp_dir)

        rename = rename_class_mock(image_path=_temp_image_file, prefix="prefix", suffix="suffix")
        rename.add_prefix_suffix()
        assert rename.renamed_image_name == _after

    def test_add_serial_number(self, temp_image_file, temp_dir_path, rename_class_mock):
        # missing is_serial_number_added, loop_count, zero_padding_digit
        _before = "image.png"
        _after = "image001.png"
        _dir_path = temp_dir_path()
        _temp_image_file: pathlib.Path = temp_image_file(image_path=_before, temp_dir_path=_dir_path)

        # check default values of args
        rename = rename_class_mock(image_path=_temp_image_file, is_serial_number_added=False, loop_count=None)
        assert rename.is_serial_number_added is False
        assert rename.loop_count is None
        assert rename.zero_padding_digit == DefaultValues.ZERO_PADDING_DIGIT.value

        with pytest.raises(ValueError) as excinfo:
            rename.add_serial_number()
        assert excinfo.value.args[0] == "'loop_count' should be start from 1."

        # is_serial_number_added is False
        rename = rename_class_mock(image_path=_temp_image_file)
        rename.add_serial_number()
        assert rename.renamed_image_name == _before

        # loop_count is 0
        rename = rename_class_mock(image_path=_temp_image_file, is_serial_number_added=True, loop_count=0)
        with pytest.raises(ValueError) as excinfo:
            rename.add_serial_number()
        assert excinfo.value.args[0] == "'loop_count' should be start from 1."

        # ok
        rename = rename_class_mock(image_path=_temp_image_file, is_serial_number_added=True)
        rename.add_serial_number()
        assert rename.renamed_image_name == _after

        # if is_all_replaced_with_new_name is True and is_serial_number_added is False
        # serial numbers should be added.
        rename = rename_class_mock(
            image_path=_temp_image_file, is_serial_number_added=False, is_all_replaced_with_new_name=True
        )
        rename.add_serial_number()
        assert rename.renamed_image_name == _after

    def test_replace_unavailable_file_name_characters_in_windows(self, temp_image_file, rename_class_mock):
        if is_os_windows():
            return
        _temp_dir: pathlib.Path = rename_class_mock.dir_path
        _before = ':*?"<>|¥.png'
        _after = "--------.png"
        _temp_image_file: pathlib.Path = temp_image_file(image_path=_before, temp_dir_path=_temp_dir)
        rename = rename_class_mock(image_path=_temp_image_file)
        assert hasattr(rename.__class__, "unavailable_char_in_windows_pattern") is True
        assert hasattr(rename, "unavailable_char_in_windows_pattern") is True
        assert type(rename.unavailable_char_in_windows_pattern) is re.Pattern
        assert (
            rename.alternative_unavailable_char_in_windows
            == DefaultValues.ALTERNATIVE_UNAVAILABLE_CHAR_IN_WINDOWS.value
        )
        rename.replace_unavailable_file_name_chars()
        assert rename.renamed_image_name == _after

    def test_replace_url_encoded_characters(self, temp_image_file, rename_class_mock):
        _temp_dir: pathlib.Path = rename_class_mock.dir_path
        _before = ",!()abc123-_あ &^%.png"
        _after = "XXXXabc123-_XXXXX.png"
        _temp_image_file: pathlib.Path = temp_image_file(image_path=_before, temp_dir_path=_temp_dir)

        # missing is_url_encoded_char_replaced,
        # alternative_url_encoded_char
        # and url_encoded_char_pattern
        rename = rename_class_mock(image_path=_temp_image_file)
        rename.replace_url_encoded_chars()
        assert rename.renamed_image_name == _before

        # not replace
        rename = rename_class_mock(image_path=_temp_image_file, is_url_encoded_char_replaced=False)
        rename.replace_url_encoded_chars()
        assert rename.renamed_image_name == _before

        # replace
        rename = rename_class_mock(image_path=_temp_image_file, is_url_encoded_char_replaced=True)
        rename.replace_url_encoded_chars()
        assert rename.renamed_image_name == _after

    def test_recursively_create_directories(self, temp_image_file, rename_class_mock):
        ######################################
        # root
        #  |-- root_img.png
        #  |-- dir1
        #       | -- dir1_img.png
        #       | -- dir2
        #             |-- dir2.img.png
        ######################################
        _temp_dir: pathlib.Path = rename_class_mock.dir_path
        _root_img = "root_img.png"
        _dir1_img = "dir1/dir1_img.png"
        _dir2_img = "dir1/dir2/dir2_img.png"
        _root_img_path: pathlib.Path = temp_image_file(image_path=_root_img, temp_dir_path=_temp_dir)
        _dir1_img_path: pathlib.Path = temp_image_file(image_path=_dir1_img, temp_dir_path=_temp_dir)
        _dir2_img_path: pathlib.Path = temp_image_file(image_path=_dir2_img, temp_dir_path=_temp_dir)

        # root dir exists.
        rename = rename_class_mock(image_path=_root_img_path, run=True, is_output_to_same_dir=False)
        rename.rename()

        # check name changed correctly
        assert rename.renamed_image_name == _root_img_path.name

        # check renamed image parent paths
        assert rename.renamed_relative_image_parent_path.exists() is True
        assert rename.renamed_relative_image_parent_path.is_dir() is True
        assert rename.renamed_relative_image_parent_path.as_posix() == rename.dest_dir_path.as_posix()

        # check renamed image. name
        assert rename.renamed_image_path.samefile(rename.renamed_relative_image_path)
        assert rename.renamed_image_path.as_posix() == rename.renamed_relative_image_path.as_posix()
        assert rename.renamed_image_path.exists() is True
        assert rename.renamed_image_path.is_file() is True

        # check original image exists.
        assert rename.original_image_name == _root_img_path.name
        assert rename.image_path.exists() is True
        assert rename.image_path.is_file() is True
        assert rename.image_path.as_posix() == _root_img_path.as_posix()

        # dir1 exists.
        rename = rename_class_mock(image_path=_dir1_img_path, run=True)
        rename.rename()

        # check name changed correctly
        assert rename.renamed_image_name == _dir1_img_path.name

        # check renamed image parent paths
        _dir1_img_parent: pathlib.Path = pathlib.Path(rename.dest_dir_path / _dir1_img).parent
        assert rename.renamed_relative_image_parent_path.as_posix() == _dir1_img_parent.as_posix()
        assert rename.renamed_relative_image_parent_path.exists() is True
        assert rename.renamed_relative_image_parent_path.is_dir() is True

        # check renamed image
        assert rename.renamed_image_path.samefile(rename.renamed_relative_image_path)
        assert rename.renamed_image_path.as_posix() == rename.renamed_relative_image_path.as_posix()
        assert rename.renamed_image_path.exists() is True
        assert rename.renamed_image_path.is_file() is True

        # check original image exists.
        assert rename.original_image_name == _dir1_img_path.name
        assert rename.image_path.exists() is True
        assert rename.image_path.is_file() is True
        assert rename.image_path.as_posix() == _dir1_img_path.as_posix()

        # dir2 exists.
        rename = rename_class_mock(image_path=_dir2_img_path, run=True)
        rename.rename()

        # check name changed correctly
        assert rename.renamed_image_name == _dir2_img_path.name

        # check renamed image parent paths
        _dir2_img_parent: pathlib.Path = pathlib.Path(rename.dest_dir_path / _dir2_img).parent
        assert rename.renamed_relative_image_parent_path.as_posix() == _dir2_img_parent.as_posix()
        assert rename.renamed_relative_image_parent_path.exists() is True
        assert rename.renamed_relative_image_parent_path.is_dir() is True

        # check renamed image
        assert rename.renamed_image_path.samefile(rename.renamed_relative_image_path)
        assert rename.renamed_image_path.as_posix() == rename.renamed_relative_image_path.as_posix()
        assert rename.renamed_image_path.exists() is True
        assert rename.renamed_image_path.is_file() is True

        # check original image exists.
        assert rename.original_image_name == _dir2_img_path.name
        assert rename.image_path.exists() is True
        assert rename.image_path.is_file() is True
        assert rename.image_path.as_posix() == _dir2_img_path.as_posix()

    def test_output_to_the_same_dir(self, temp_image_file, rename_class_mock):
        ######################################
        # root
        #  |-- root_img.png
        #  |-- dir1
        #       | -- dir1_img.png
        #       | -- dir2
        #             |-- dir2.img.png
        ######################################
        _temp_dir: pathlib.Path = rename_class_mock.dir_path
        _root_img = "root_img.png"
        _dir1_img = "dir1/dir1_img.png"
        _dir2_img = "dir1/dir2/dir2_img.png"
        _root_img_path: pathlib.Path = temp_image_file(image_path=_root_img, temp_dir_path=_temp_dir)
        _dir1_img_path: pathlib.Path = temp_image_file(image_path=_dir1_img, temp_dir_path=_temp_dir)
        _dir2_img_path: pathlib.Path = temp_image_file(image_path=_dir2_img, temp_dir_path=_temp_dir)

        # root dir.
        rename = rename_class_mock(image_path=_root_img_path, run=True, is_output_to_same_dir=True)
        rename.rename()

        # check name changed correctly
        assert rename.renamed_image_name == _root_img_path.name

        # check renamed image parent paths
        assert rename.renamed_relative_image_parent_path.as_posix() == rename.dest_dir_path.as_posix()
        assert rename.renamed_relative_image_parent_path.exists() is True  # root
        assert rename.renamed_relative_image_parent_path.is_dir() is True

        # check renamed image.
        assert rename.renamed_image_path.samefile(rename.renamed_relative_image_path) is True
        assert rename.renamed_image_path.samefile(rename.renamed_image_path_in_same_dir) is True
        assert rename.renamed_image_path.as_posix() == rename.renamed_image_path_in_same_dir.as_posix()
        assert rename.renamed_relative_image_path.as_posix() == rename.renamed_image_path_in_same_dir.as_posix()
        assert rename.dirs_prefix == ""
        assert rename.renamed_image_path.exists() is True
        assert rename.renamed_image_path.is_file() is True

        # check original image exists.
        assert rename.original_image_name == _root_img_path.name
        assert rename.image_path.exists() is True
        assert rename.image_path.is_file() is True
        assert rename.image_path.as_posix() == _root_img_path.as_posix()

        # dir1 exists.
        rename = rename_class_mock(image_path=_dir1_img_path, run=True, is_output_to_same_dir=True)
        rename.rename()

        # check name changed correctly
        assert rename.renamed_image_name != _dir1_img_path.name  # should add dir prefix
        assert rename.renamed_image_name == f"{rename.dirs_prefix}{_dir1_img_path.name}"

        # check renamed image parent paths
        _dir1_img_parent: pathlib.Path = pathlib.Path(rename.dest_dir_path / _dir1_img).parent
        assert rename.renamed_relative_image_parent_path.as_posix() == _dir1_img_parent.as_posix()
        assert rename.renamed_relative_image_parent_path.exists() is False
        assert rename.renamed_relative_image_parent_path.is_dir() is False

        # check renamed image
        with pytest.raises(FileNotFoundError) as excinfo:
            assert rename.renamed_image_path.samefile(rename.renamed_relative_image_path) is False
        assert excinfo.type is FileNotFoundError
        if is_os_windows():
            assert excinfo.value.strerror == "The system cannot find the path specified"
        else:
            assert excinfo.value.strerror == "No such file or directory"
        assert rename.renamed_image_path.as_posix() != rename.renamed_relative_image_path.as_posix()

        assert rename.renamed_image_path.as_posix() == rename.renamed_image_path_in_same_dir.as_posix()
        assert (
            rename.renamed_image_path.as_posix()
            == rename.dest_dir_path.as_posix() + f"/{rename.dirs_prefix}{_dir1_img_path.name}"
        )
        assert rename.renamed_image_path.exists() is True
        assert rename.renamed_image_path.is_file() is True

        # check original image exists.
        assert rename.original_image_name == _dir1_img_path.name
        assert rename.image_path.exists() is True
        assert rename.image_path.is_file() is True
        assert rename.image_path.as_posix() == _dir1_img_path.as_posix()

        # dir2 exists.
        rename = rename_class_mock(image_path=_dir2_img_path, run=True, is_output_to_same_dir=True)
        rename.rename()

        # check name changed correctly
        assert rename.renamed_image_name != _dir2_img_path.name  # should add dir prefix
        assert rename.renamed_image_name == f"{rename.dirs_prefix}{_dir2_img_path.name}"

        # check renamed image parent paths
        # not make dirs recursively
        _dir2_img_parent: pathlib.Path = pathlib.Path(rename.dest_dir_path / _dir2_img).parent
        assert rename.renamed_relative_image_parent_path.as_posix() == _dir2_img_parent.as_posix()
        assert rename.renamed_relative_image_parent_path.exists() is False
        assert rename.renamed_relative_image_parent_path.is_dir() is False

        # check renamed image
        with pytest.raises(FileNotFoundError) as excinfo:
            assert rename.renamed_image_path.samefile(rename.renamed_relative_image_path) is False
        assert excinfo.type is FileNotFoundError
        if is_os_windows():
            assert excinfo.value.strerror == "The system cannot find the path specified"
        else:
            assert excinfo.value.strerror == "No such file or directory"
        assert rename.renamed_image_path.as_posix() != rename.renamed_relative_image_path.as_posix()

        assert rename.renamed_image_path.as_posix() == rename.renamed_image_path_in_same_dir.as_posix()
        assert (
            rename.renamed_image_path.as_posix()
            == rename.dest_dir_path.as_posix() + f"/{rename.dirs_prefix}{_dir2_img_path.name}"
        )
        assert rename.renamed_image_path.exists() is True
        assert rename.renamed_image_path.is_file() is True

        # check original image exists.
        assert rename.original_image_name == _dir2_img_path.name
        assert rename.image_path.exists() is True
        assert rename.image_path.is_file() is True
        assert rename.image_path.as_posix() == _dir2_img_path.as_posix()

    def test_make_comparison_files(self, temp_image_file, rename_class_mock):
        _count: int = 10
        for index in range(1, _count + 1):
            _temp_dir: pathlib.Path = rename_class_mock.dir_path
            _image_path = f"{index}.png"
            _temp_image_file: pathlib.Path = temp_image_file(image_path=_image_path, temp_dir_path=_temp_dir)
            rename = rename_class_mock(image_path=_temp_image_file, loop_count=index, run=True)
            rename.rename()
            assert rename.comparison_length == index
            assert rename.comparison_log[-1] == rename.comparison
        else:
            assert len(rename_class_mock.comparison_log) == _count

            # comparison_log will be clear after make_comparison_file is called.
            _text = "\n\n".join(rename_class_mock.comparison_log)

            # make file.
            _dest_dir = rename_class_mock.get_dest_dir_path(
                now_str=rename.now_str, dir_path=rename.dir_path, dest=rename.dest
            )
            rename_class_mock.make_comparison_file(dest_dir_path=_dest_dir)

            # check created comparison file.
            comparison_file_path = _dest_dir / DefaultValues.COMPARISON_FILE_NAME.value
            assert comparison_file_path.exists() is True
            assert comparison_file_path.is_file() is True
            assert comparison_file_path.read_text() == _text

            # ensure that comparison log is initialized.
            assert type(rename_class_mock.comparison_log) is list
            assert len(rename_class_mock.comparison_log) == 0
