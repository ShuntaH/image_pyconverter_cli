import os
import shutil
import subprocess

import pytest

from lib import get_image_paths
from lib.rename import DefaultValues, Rename
from utils.stdout import Stdout, Bcolors
from utils.tests import TEST_IMAGE_DIR_PATH


@pytest.fixture
def temp_dir_path_for_renamed_images(temp_image_dir_path):
    return f"{temp_image_dir_path}/RENAMED_IMAGES"
class TestRename:


    @classmethod
    def setup_class(cls):
        Stdout.styled_stdout(Bcolors.HEADER.value, f'Setup {cls.__name__} class.')
        cls.images_dir_path = TEST_IMAGE_DIR_PATH
        cls.image_path = get_image_paths(dir_path=cls.images_dir_path)[0]  # './src/tests/images/bar_foo_fuga.png

    def teardown_method(self, method):
        """Directories created during testing are deleted after the test is completed."""
        shutil.rmtree(self.temp_renamed_images_dir_path)
        Stdout.styled_stdout(
            Bcolors.OKCYAN.value,
            f'removed the temp directory {self.temp_renamed_images_dir_path}. \nteardown_method done.'
        )

    def
    def test_renamed_images_dir_path_exist(self):
        rename = Rename(image_path=self.image_path)
        assert os.path.exists(self.temp_renamed_images_dir_path) is True
        assert rename.renamed_images_dir_path == self.temp_renamed_images_dir_path

    def test_replace_words(self):
        words_before_replacement: list[str] = ['bar', 'foo', 'fuga']
        words_after_replacement: list[str] = ['replaced-bar', 'replaced-foo', 'replaced-fuga']

        orig = 'bar_foo_fuga'
        rename = Rename(
            image_path=self.image_path,
            words_before_replacement=words_before_replacement,
            words_after_replacement=words_after_replacement
        )
        assert orig == rename.renamed_image_name

        rename.replace_words()
        expected = 'replaced-bar_replaced-foo_replaced-fuga'
        assert expected == rename.renamed_image_name

        # subprocess.run(['ic_rename', abs_image_paths])

    def test_replace_the_number_of_missing_words_before_replacement(self):
        # short of words_before_replacement
        words_before_replacement: list[str] = ['bar']
        words_after_replacement: list[str] = ['replaced-bar', 'replaced-foo', 'replaced-fuga']

        orig = 'bar_foo_fuga'
        expected = 'replaced-bar_foo_fuga'
        rename = Rename(
            image_path=self.image_path,
            words_before_replacement=words_before_replacement,
            words_after_replacement=words_after_replacement
        )
        assert rename.renamed_image_name == orig
        rename.replace_words()
        assert expected == rename.renamed_image_name

    def test_replace_the_number_of_missing_words_after_replacement(self):
        # short of words_after_replacement
        words_before_replacement: list[str] = ['bar', 'foo', 'fuga']
        words_after_replacement: list[str] = ['replaced-bar']

        orig = 'bar_foo_fuga'
        expected = 'replaced-bar_foo_fuga'
        rename = Rename(
            image_path=self.image_path,
            words_before_replacement=words_before_replacement,
            words_after_replacement=words_after_replacement
        )
        assert rename.renamed_image_name == orig
        rename.replace_words()
        assert expected == rename.renamed_image_name

    def test_replace_full_width_characters_with_half_width(self):
        """
        name００１.png => name001.png
        """
        pass

    def test_replace_delimiters_with_specified_separator():
        pass

    def test_replace_unavailable_characters():
        pass

    def test_replace_invalid_url_characters():
        pass

    def test_add_prefix_and_suffix():
        pass

    def test_enable_to_add_serial_number():
        pass

    def test_is_extensions_valid():
        pass

    def test_enable_to_rename():
        pass

    def test_enable_to_make_name_files():
        pass
