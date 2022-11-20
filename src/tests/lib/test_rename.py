import os

from lib.rename import Rename


class TestRename:
    def test_renamed_images_dir_path_exist(self, temp_dir, temp_image_file):
        rename = Rename(image_path=temp_image_file('test.png'))
        assert os.path.exists(self.temp_renamed_images_dir_path) is True
        assert rename.dest == temp_dir

    # def test_replace_words(self):
    #     words_before_replacement: list[str] = ['bar', 'foo', 'fuga']
    #     words_after_replacement: list[str] = ['replaced-bar', 'replaced-foo', 'replaced-fuga']
    #
    #     orig = 'bar_foo_fuga'
    #     rename = Rename(
    #         image_path=self.image_path,
    #         words_before_replacement=words_before_replacement,
    #         words_after_replacement=words_after_replacement
    #     )
    #     assert orig == rename.renamed_image_name
    #
    #     rename.replace_words()
    #     expected = 'replaced-bar_replaced-foo_replaced-fuga'
    #     assert expected == rename.renamed_image_name
    #
    #     # subprocess.run(['ic_rename', abs_image_paths])
    #
    # def test_replace_the_number_of_missing_words_before_replacement(self):
    #     # short of words_before_replacement
    #     words_before_replacement: list[str] = ['bar']
    #     words_after_replacement: list[str] = ['replaced-bar', 'replaced-foo', 'replaced-fuga']
    #
    #     orig = 'bar_foo_fuga'
    #     expected = 'replaced-bar_foo_fuga'
    #     rename = Rename(
    #         image_path=self.image_path,
    #         words_before_replacement=words_before_replacement,
    #         words_after_replacement=words_after_replacement
    #     )
    #     assert rename.renamed_image_name == orig
    #     rename.replace_words()
    #     assert expected == rename.renamed_image_name
    #
    # def test_replace_the_number_of_missing_words_after_replacement(self):
    #     # short of words_after_replacement
    #     words_before_replacement: list[str] = ['bar', 'foo', 'fuga']
    #     words_after_replacement: list[str] = ['replaced-bar']
    #
    #     orig = 'bar_foo_fuga'
    #     expected = 'replaced-bar_foo_fuga'
    #     rename = Rename(
    #         image_path=self.image_path,
    #         words_before_replacement=words_before_replacement,
    #         words_after_replacement=words_after_replacement
    #     )
    #     assert rename.renamed_image_name == orig
    #     rename.replace_words()
    #     assert expected == rename.renamed_image_name

    def test_replace_full_width_characters_with_half_width(self):
        """
        name００１.png => name001.png
        """
        pass

    def test_replace_delimiters_with_specified_separator(self):
        pass

    def test_replace_unavailable_characters(self):
        pass

    def test_replace_invalid_url_characters(self):
        pass

    def test_add_prefix_and_suffix(self):
        pass

    def test_enable_to_add_serial_number(self):
        pass

    def test_is_extensions_valid(self):
        pass

    def test_enable_to_rename(self):
        pass

    def test_enable_to_make_name_files(self):
        pass
