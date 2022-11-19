import os
import shutil
import subprocess

from src.lib import get_image_paths
from src.lib.rename import DefaultValues, Rename
from src.utils import tests
from src.utils.stdout import Stdout, Bcolors


class TestRename:
    temp_renamed_images_dir_path = f"{tests.get_images_dir_path()}/{DefaultValues.RENAMED_IMAGES_DIR_NAME.value}"

    @classmethod
    def setup_class(cls):
        cls.images_dir_path = tests.get_images_dir_path()
        cls.image_path = get_image_paths(dir_path=cls.images_dir_path)[0]  # './src/tests/images/bar_foo_fuga.png

    def teardown_method(self):
        """Directories created during testing are deleted after the test is completed."""
        shutil.rmtree(self.temp_renamed_images_dir_path)
        Stdout.styled_stdout(
            Bcolors.OKCYAN.value, 'removed the temp directory. \nteardown_method done.')

    def test_renamed_images_dir_path_exist(self):
        rename = Rename(image_path=self.image_path)
        assert os.path.exists(self.temp_renamed_images_dir_path) is True
        assert rename.renamed_images_dir_path == self.temp_renamed_images_dir_path

    def test_enable_to_replace_words(self):
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

    def test_replace_different_number_words(self):
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
