import pathlib

from lib.rename import Rename


class TestRename:
    def test_post_init(self, temp_dir_path, temp_image_file, temp_dest_path):
        _temp_dir: pathlib.Path = temp_dir_path()
        _temp_image_file: pathlib.Path = temp_image_file(
            image_name='post_init_test.png',
            temp_dir_path=_temp_dir
        )
        _temp_dest: pathlib.Path = temp_dest_path()

        rename = Rename(image_path=_temp_image_file, dest=_temp_dest)

        assert rename.dir_path == _temp_dir
        assert rename.relative_dir_path == _temp_dir.relative_to(_temp_dir)
        assert rename.relative_image_path == _temp_image_file.relative_to(_temp_dir)
        assert rename.relative_image_parent_path == rename.relative_image_path.parents[0]
        assert rename.original_image_name == _temp_image_file.name
        assert rename.ext == ''.join(_temp_image_file.suffixes)
        assert rename.original_image_stem == _temp_image_file.stem
        assert rename.renamed_image_stem == _temp_image_file.stem
        assert rename.zero_padding_string == '{{0:0{}d}}'.format(rename.zero_padding_digit)
        assert rename.dest == _temp_dest
        assert rename.dest_dir_path == _temp_dest / rename.dest_dir_name
        assert rename.dest_dir_path.exists() is True

    def test_replace_words(self, temp_dir_path, temp_image_file):
        _temp_dir: pathlib.Path = temp_dir_path()

        _before = 'bar_foo_fuga.png'
        _temp_image_file: pathlib.Path = temp_image_file(
            image_name=_before,
            temp_dir_path=_temp_dir
        )

        _after = 'replaced-bar_replaced-foo_replaced-fuga.png'
        words_before_replacement: list[str] = ['bar', 'foo', 'fuga']
        words_after_replacement: list[str] = ['replaced-bar', 'replaced-foo', 'replaced-fuga']

        rename = Rename(
            image_path=_temp_image_file,
            words_before_replacement=words_before_replacement,
            words_after_replacement=words_after_replacement
        )
        rename.replace_words()
        assert rename.renamed_image_name == _after

        # short of words_before_replacement
        _after = 'replaced-bar_foo_fuga.png'
        words_before_replacement: list[str] = ['bar']
        words_after_replacement: list[str] = ['replaced-bar', 'replaced-foo', 'replaced-fuga']
        rename = Rename(
            image_path=_temp_image_file,
            words_before_replacement=words_before_replacement,
            words_after_replacement=words_after_replacement
        )
        rename.replace_words()
        assert rename.renamed_image_name == _after

        # short of words_after_replacement
        _after = 'replaced-bar_foo_fuga.png'
        words_before_replacement: list[str] = ['bar', 'foo', 'fuga']
        words_after_replacement: list[str] = ['replaced-bar']
        rename = Rename(
            image_path=_temp_image_file,
            words_before_replacement=words_before_replacement,
            words_after_replacement=words_after_replacement
        )
        rename.replace_words()
        assert rename.renamed_image_name == _after

        # words_before_replacement is empty
        words_before_replacement: list[str] = list()
        words_after_replacement: list[str] = ['replaced-bar']
        rename = Rename(
            image_path=_temp_image_file,
            words_before_replacement=words_before_replacement,
            words_after_replacement=words_after_replacement
        )
        rename.replace_words()
        assert rename.renamed_image_name == _before

        # words_after_replacement is empty
        words_before_replacement: list[str] = ['bar', 'foo']
        words_after_replacement: list[str] = list()
        rename = Rename(
            image_path=_temp_image_file,
            words_before_replacement=words_before_replacement,
            words_after_replacement=words_after_replacement
        )
        rename.replace_words()
        assert rename.renamed_image_name == _before

        # subprocess.run(['ic_rename', abs_image_paths])

    def test_replace_full_width_characters_with_half_width(
            self,
            temp_dir_path,
            temp_image_file
    ):
        """
        name００１.png => name001.png
        """
        _temp_dir: pathlib.Path = temp_dir_path()

        # half-width ASCII characters don't change.
        _before = 'half_width.png'
        _temp_image_file: pathlib.Path = temp_image_file(
            image_name=_before,
            temp_dir_path=_temp_dir
        )

        rename = Rename(image_path=_temp_image_file)
        rename.zen2han()
        assert rename.renamed_image_name == _before

        # full-width ASCII characters to half-width
        _before = 'ｆｕｌｌｗｉｄｔｈ.png'
        _after = 'fullwidth.png'
        _temp_image_file: pathlib.Path = temp_image_file(
            image_name=_before,
            temp_dir_path=_temp_dir
        )

        rename = Rename(image_path=_temp_image_file)
        rename.zen2han()
        assert rename.renamed_image_name == _after

        # Non-ASCII characters are not converted to half-width characters.
        _before = '全角.png'
        _temp_image_file: pathlib.Path = temp_image_file(
            image_name=_before,
            temp_dir_path=_temp_dir
        )

        rename = Rename(image_path=_temp_image_file)
        rename.zen2han()
        assert rename.renamed_image_name == _before

        # half-width numbers don't change.
        _before = '123.png'
        _temp_image_file: pathlib.Path = temp_image_file(
            image_name=_before,
            temp_dir_path=_temp_dir
        )

        rename = Rename(image_path=_temp_image_file)
        rename.zen2han()
        assert rename.renamed_image_name == _before

        # full-width numbers to half-width
        _before = '１２３.png'
        _after = '123.png'
        _temp_image_file: pathlib.Path = temp_image_file(
            image_name=_before,
            temp_dir_path=_temp_dir
        )

        rename = Rename(image_path=_temp_image_file)
        rename.zen2han()
        assert rename.renamed_image_name == _after

        # full width space to half width space.
        _before = 'ｓｐａｃｅ　ｓｐａｃｅ.png'
        _after = 'space space.png'
        _temp_image_file: pathlib.Path = temp_image_file(
            image_name=_before,
            temp_dir_path=_temp_dir
        )

        rename = Rename(image_path=_temp_image_file)
        rename.zen2han()
        assert rename.renamed_image_name == _after

    def test_replace_delimiters_with_specified_separator(
            self, temp_dir_path, temp_image_file
    ):
        _temp_dir: pathlib.Path = temp_dir_path()

        # replace half width space with a separator
        _before = 'space space.png'
        _after = 'space_space.png'
        _temp_image_file: pathlib.Path = temp_image_file(
            image_name=_before,
            temp_dir_path=_temp_dir
        )

        rename = Rename(image_path=_temp_image_file)
        rename.replace_with_separator()
        assert rename.renamed_image_name == _after

        # replace full width space with a separator
        _before = 'space　space.png'
        _after = 'space_space.png'
        _temp_image_file: pathlib.Path = temp_image_file(
            image_name=_before,
            temp_dir_path=_temp_dir
        )

        rename = Rename(image_path=_temp_image_file)
        rename.replace_with_separator()
        assert rename.renamed_image_name == _after

        # replace tab space with a separator
        _before = 'space    space.png'
        _after = 'space____space.png'
        _temp_image_file: pathlib.Path = temp_image_file(
            image_name=_before,
            temp_dir_path=_temp_dir
        )

        rename = Rename(image_path=_temp_image_file)
        rename.replace_with_separator()
        assert rename.renamed_image_name == _after

        # replace '.' with a separator
        # '.' looks some file extension.
        _before = 'space.space.png'
        _after = 'space_space.png'
        _temp_image_file: pathlib.Path = temp_image_file(
            image_name=_before,
            temp_dir_path=_temp_dir
        )

        rename = Rename(image_path=_temp_image_file)
        rename.replace_with_separator()
        assert rename.renamed_image_name == _after

        # replace ',' with a separator
        _before = 'space,space.png'
        _after = 'space_space.png'
        _temp_image_file: pathlib.Path = temp_image_file(
            image_name=_before,
            temp_dir_path=_temp_dir
        )

        rename = Rename(image_path=_temp_image_file)
        rename.replace_with_separator()
        assert rename.renamed_image_name == _after

        # replace '-' with a separator
        _before = 'space,space.png'
        _after = 'space_space.png'
        _temp_image_file: pathlib.Path = temp_image_file(
            image_name=_before,
            temp_dir_path=_temp_dir
        )

        rename = Rename(image_path=_temp_image_file)
        rename.replace_with_separator()
        assert rename.renamed_image_name == _after

        # replace ',' with a separator
        _before = 'space,space.png'
        _after = 'space_space.png'
        _temp_image_file: pathlib.Path = temp_image_file(
            image_name=_before,
            temp_dir_path=_temp_dir
        )

        rename = Rename(image_path=_temp_image_file)
        rename.replace_with_separator()
        assert rename.renamed_image_name == _after

        # replace 'ー' with a separator
        _before = 'spaceーspace.png'
        _after = 'space_space.png'
        _temp_image_file: pathlib.Path = temp_image_file(
            image_name=_before,
            temp_dir_path=_temp_dir
        )

        rename = Rename(image_path=_temp_image_file)
        rename.replace_with_separator()
        assert rename.renamed_image_name == _after



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
