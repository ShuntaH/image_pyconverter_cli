import os
import shutil
import subprocess
import tempfile

from lib import get_image_paths
from lib.rename import Rename, DefaultValues
from utils import tests
from utils.stdout import Stdout, Bcolors


class TestRename:
    temp_renamed_images_dir_path = f"{tests.get_images_dir_path()}/{DefaultValues.RENAMED_IMAGES_DIR_NAME.value}"

    @classmethod
    def teardown_method(cls):
        """Directories created during testing are deleted after the test is completed."""
        shutil.rmtree(cls.temp_renamed_images_dir_path)
        Stdout.styled_stdout(
            Bcolors.OKCYAN.value, 'removed the temp directory. \nteardown_method done.')

    def test_renamed_images_dir_path_exist(self):
        image_path = get_image_paths(dir_path=tests.get_images_dir_path())[0]  # './src/tests/images/food_protein_bar
        # .png'
        rename = Rename(image_path=image_path)
        assert os.path.exists(self.temp_renamed_images_dir_path) is True
        assert rename.renamed_images_dir_path == self.temp_renamed_images_dir_path

    def test_enable_to_replace_words(self):
        image_path = get_image_paths(dir_path=tests.get_images_dir_path())[0]  # './src/tests/images/food_protein_bar
        # .png'
        words_before_replacement: list[str] = ['bar', 'foo', 'fuga']
        words_after_replacement: list[str] = ['replaced-bar', 'replaced-foo', 'replaced-fuga']

        orig = 'bar_foo_fuga'
        rename = Rename(
            image_path=image_path,
            words_before_replacement=words_before_replacement,
            words_after_replacement=words_after_replacement
        )
        assert rename.renamed_image_name == orig

        rename.replace_words()
        expected = 'replaced-bar_replaced-foo_replaced-fuga'
        assert expected == rename.renamed_image_name

        # subprocess.run(['ic_rename', abs_image_paths])

        pass


def test_enable_to_replace_full_width_characters_with_half_width():
    # todo jacovモジュールの中身から全角を半角に直すところを取り出してそれをテストする
    pass


def test_enable_to_replace_delimiters_with_specified_separator():
    pass


def test_enable_to_replace_unavailable_characters():
    pass


def test_enable_to_replace_invalid_url_characters():
    pass


def test_enable_to_add_prefix_and_suffix():
    pass


def test_enable_to_add_serial_number():
    pass


def test_is_extensions_valid():
    pass


def test_enable_to_rename():
    pass


def test_enable_to_make_name_files():
    pass
