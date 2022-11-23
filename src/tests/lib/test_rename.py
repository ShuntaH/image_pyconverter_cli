import pathlib

from lib.rename import Rename


class TestRename:
    def test_post_init(self, temp_dir_path, temp_image_file, temp_dest):
        _temp_dir_path: pathlib.Path = temp_dir_path()
        _temp_image_file: pathlib.Path = temp_image_file(
            image_name='post_init_test.png',
            temp_dir_path=_temp_dir_path
        )
        _temp_dest: pathlib.Path = temp_dest()

        rename = Rename(image_path=_temp_image_file, dest=_temp_dest)

        assert rename.dir_path == _temp_dir_path
        assert rename.relative_dir_path == _temp_dir_path.relative_to(_temp_dir_path)
        assert rename.relative_image_path == _temp_image_file.relative_to(_temp_dir_path)
        assert rename.relative_image_parent_path == rename.relative_image_path.parents[0]
        assert rename.original_image_name == _temp_image_file.name
        assert rename.ext == ''.join(_temp_image_file.suffixes)
        assert rename.original_image_stem == _temp_image_file.stem
        assert rename.renamed_image_stem == _temp_image_file.stem
        assert rename.zero_padding_string == '{{0:0{}d}}'.format(rename.zero_padding_digit)
        assert rename.dest == _temp_dest
        assert rename.dest_root == _temp_dest / rename.dest_dir_name
        assert rename.dest_root.exists() is True


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
