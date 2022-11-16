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


def test_enable_to_replace_words():
    with tempfile.TemporaryDirectory() as td:
        """
        一時的なディレクトリを作成する
        """
        print(td)
    # subprocess.run(['ic_rename', abs_image_paths])
    # rename = Rename(
    #     image_path=image_path,
    #     words_before_replacement=args.words_before_replacement,
    #     words_after_replacement=args.words_after_replacement,
    #     prefix=args.prefix,
    #     suffix=args.suffix,
    #     replacement_with_separator_pattern=args.replacement_with_separator_pattern,
    #     separator=args.separator,
    #     unavailable_file_name_char_pattern=args.unavailable_file_name_char_pattern,
    #     alternative_unavailable_file_name_char=args.unavailable_file_name_char,
    #     is_unavailable_url_chars_kept=args.is_unavailable_url_chars_kept,
    #     alternative_unavailable_url_char=args.alternative_unavailable_url_char,
    #     unavailable_url_char_pattern=args.unavailable_url_char_pattern,
    #     is_serial_number_added=args.is_serial_number_added,
    #     current_index=index,
    #     zero_padding_digit=args.serial_number_zero_padding_digit,
    #     valid_extensions=args.valid_extensions
    # )
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
