import argparse
import enum
import pathlib
import re
import dataclasses
import shutil
import tempfile
from typing import Optional, Pattern, ClassVar, Union

from jaconv import jaconv

from src.utils.stdout import Stdout, Bcolors
from src.utils.with_statements import task, add_extra_arguments_to
from utils import get_image_paths_from_within, datetime2str
from utils.rename import validate_replacement_with_separator_pattern_arg


class DefaultValues(enum.Enum):
    DEST_DIR_NAME = f"RENAMED_IMAGES_{datetime2str()}"
    DEST = pathlib.Path.cwd()

    PREFIX = ''
    SUFFIX = ''

    REPLACEMENT_WITH_SEPARATOR_PATTERN = re.compile(r'[ 　\t\n.,\-ー_＿]')
    SEPARATOR = '_'

    ###########################################################
    # Characters that cannot be used in file names.
    # windows /:*?"<>|¥
    # mac /
    # On mac, "/" cannot be used in filenames because it is a path separator.
    # finder can use "/", but if you look at the filename in a shell,
    # you will see ":".
    ###########################################################
    UNAVAILABLE_FILE_NAME_CHAR_PATTERN = re.compile(r'[\/:*?"<>|¥]')
    ALTERNATIVE_UNAVAILABLE_FILE_NAME_CHAR = '-'

    URL_ENCODED_CHAR_PATTERN = re.compile(r'[^-_a-zA-Z0-9]')
    ALTERNATIVE_URL_ENCODED_CHAR = 'X'

    ZERO_PADDING_DIGIT = 3

    VALID_EXTENSIONS = [
        '.jpg',
        '.jpeg',
        '.JPG',
        '.JPEG',
        '.jpe',
        '.jfif',
        '.pjpeg',
        '.pjp',
        '.png',
        '.gif',
        '.tiff',
        '.tif',
        '.webp',
        '.svg',
        '.svgz'
    ]

    COMPARISON_FILE_NAME = 'comparison.txt'


@dataclasses.dataclass
class Rename:

    image_path: Union[str, pathlib.Path]
    dir_path: str

    dest: Union[str, pathlib.Path] = DefaultValues.DEST.value
    dest_dir_name: str = DefaultValues.DEST_DIR_NAME.value

    chars_before_replacement: list[str] = dataclasses.field(default_factory=lambda: [])
    chars_after_replacement: list[str] = dataclasses.field(default_factory=lambda: [])

    prefix: str = DefaultValues.PREFIX.value
    suffix: str = DefaultValues.SUFFIX.value

    # not to be option.
    unavailable_file_name_char_pattern: ClassVar[Pattern] = DefaultValues.UNAVAILABLE_FILE_NAME_CHAR_PATTERN.value
    alternative_unavailable_file_name_char: str = DefaultValues.ALTERNATIVE_UNAVAILABLE_FILE_NAME_CHAR.value

    is_separator_and_delimiter_replaced: bool = False
    replacement_with_separator_pattern: Pattern = DefaultValues.REPLACEMENT_WITH_SEPARATOR_PATTERN.value
    separator: str = DefaultValues.SEPARATOR.value

    is_url_encoded_char_replaced: bool = False
    alternative_url_encoded_char: str = DefaultValues.ALTERNATIVE_URL_ENCODED_CHAR.value
    # not to be classVar
    url_encoded_char_pattern: ClassVar[Pattern] = DefaultValues.URL_ENCODED_CHAR_PATTERN.value

    is_serial_number_added: bool = False
    loop_count: Optional[int] = None
    zero_padding_digit: int = DefaultValues.ZERO_PADDING_DIGIT.value  # => 001 0001 ?
    valid_extensions: list[str] = dataclasses.field(
        default_factory=lambda: DefaultValues.VALID_EXTENSIONS.value)

    # To create a list of names of converted images,
    # each time an instance is created from this class,
    # this list is not initialized and the same list is used.
    comparison_log: ClassVar[list] = []

    is_output_to_same_dir: bool = False
    run: bool = False

    def __post_init__(self):
        if type(self.image_path) is str:
            self.image_path: pathlib.Path = pathlib.Path(self.image_path)
        if type(self.dest) is str:
            self.dest = pathlib.Path(self.dest)

        self.dir_path: pathlib.Path = pathlib.Path(self.dir_path)

        self.relative_dir_path = self.dir_path.relative_to(self.dir_path)  # => '.'
        self.relative_image_path = self.image_path.relative_to(self.dir_path)  # => './temp/img.png'
        self.relative_image_parent_path = self.relative_image_path.parent  # => './temp/

        self.original_image_name = self.image_path.name
        self.original_image_stem = self.image_path.stem

        # The name of the file to be converted may contain characters that are mistaken for file extensions.
        # In that case, the confusing name is not the file extension, so remove from image_path.suffixes
        self.ext = ''.join((
            s
            for s in self.image_path.suffixes
            if s in self.valid_extensions
        ))
        # './test.tar.gz' => ['.tar', '.gz']

        self._renamed_image_stem: str = self.original_image_stem
        self.zero_padding_string: str = '{{0:0{}d}}'.format(self.zero_padding_digit)  # => {0:03}

        self.dest_dir_path: pathlib.Path = self.dest / pathlib.Path(self.dest_dir_name)
        self.dest_dir_path.mkdir(exist_ok=True)

        if self.loop_count == 1 and self.comparison_length > 0:
            # An error may occur during the processing of multiple
            # images and the list of class variables that store the
            # names of images for recording may not be empty the next
            # time this command is executed.
            self.__class__.comparison_log = []

    @staticmethod
    def get_args():
        arg_parser = argparse.ArgumentParser()
        with add_extra_arguments_to(arg_parser) as arg_parser:
            arg_parser.add_argument(
                '-d', '--dest',
                type=str,
                help='The path where the directory containing the renamed images will be created.',
                default=DefaultValues.DEST.value
            )
            arg_parser.add_argument(
                '-ddn', '--dest_dir_name',
                type=str,
                help='The directory to which the renamed images will be output.',
                default=DefaultValues.DEST_DIR_NAME.value
            )

            arg_parser.add_argument(
                '-before', '--chars_before_replacement',
                nargs="*", type=str,
                default=[],
                help='The part of the image that will be renamed.'
            )
            arg_parser.add_argument(
                '-after', '--chars_before_replacement',
                nargs="*", type=str,
                default=[],
                help='The part of the image after being changed'
            )

            arg_parser.add_argument(
                '-p', '--prefix',
                type=str,
                help='image name prefix.',
                default=DefaultValues.PREFIX.value
            )
            arg_parser.add_argument(
                '-s', '--suffix',
                type=str,
                help='image name suffix.',
                default=DefaultValues.SUFFIX.value
            )

            arg_parser.add_argument(
                '-replace_separator_and_delimiter',
                '--is_separator_and_delimiter_replaced',
                help='Whether to unify the delimiters and separators contained in the names of images.',
                action='store_true'
            )
            arg_parser.add_argument(
                '-sep',
                '--separator',
                type=str,
                help='image name separator.',
                default=DefaultValues.SEPARATOR.value
            )
            arg_parser.add_argument(
                '-rwsp',
                '--replacement_with_separator_pattern',
                help='Regular expression pattern of characters to be replaced by separators. e.g. [^-_a-zA-Z0-9]',
                type=str,
                default='[^-_a-zA-Z0-9]'
            )

            arg_parser.add_argument(
                '-alt_ufnc',
                '--alternative_unavailable_file_name_char',
                help='A character that replaces a character that cannot be used in the name of the image.',
                type=str,
                default=DefaultValues.ALTERNATIVE_UNAVAILABLE_FILE_NAME_CHAR.value
            )

            arg_parser.add_argument(
                '-replace_url_encoded_char',
                '--is_url_encoded_char_replaced',
                help='Whether to unify the characters that are percent-encoded in the URLs contained in the image.',
                action='store_true'
            )
            arg_parser.add_argument(
                '-alt_uuc',
                '--alternative_url_encoded_char',
                help='Alternatives to characters that cannot be percent-encoded in the URL.',
                default=DefaultValues.ALTERNATIVE_URL_ENCODED_CHAR.value
            )

            arg_parser.add_argument(
                '-add_serial_number',
                '--is_serial_number_added',
                help='Whether to add the sequential number to the end of the image name.',
                action='store_true'
            )
            arg_parser.add_argument(
                '-snzpd',
                '--serial_number_zero_padding_digit',
                help='Zero padding digit of serial number.',
                type=int,
                default=DefaultValues.ZERO_PADDING_DIGIT.value
            )

            arg_parser.add_argument(
                '-ext', '--valid_extensions',
                nargs="*", type=str,
                help='.png .jpg ...',
                default=DefaultValues.VALID_EXTENSIONS.value
            )

            arg_parser.add_argument(
                '-sd',
                '--same_directory',
                help='Output to the same directory.',
                action='store_true'
            )

            args = arg_parser.parse_args()
        return args

    @property
    def renamed_image_stem(self) -> str:
        return self._renamed_image_stem

    @renamed_image_stem.setter
    def renamed_image_stem(self, image_stem: str):
        self._renamed_image_stem = image_stem

    @property
    def renamed_image_name(self) -> str:
        return f'{self.renamed_image_stem}{self.ext}'

    @property
    def renamed_relative_image_parent_path(self) -> pathlib.Path:
        return self.dest_dir_path / self.relative_image_parent_path

    @property
    def renamed_relative_image_path(self) -> pathlib.Path:
        return self.renamed_relative_image_parent_path / self.renamed_image_name

    @property
    def dirs_prefix(self) -> str:
        """
        e.g.
        root/dir1/dir2/img.png => root_dir1_dir2_
        :return:
        """
        return self.separator.join(
            self.relative_image_parent_path._parts) + self.separator

    @property
    def renamed_image_path_in_same_dir(self) -> pathlib.Path:
        return self.dest_dir_path / self.renamed_image_name

    @property
    def renamed_image_path(self) -> pathlib.Path:
        if self.is_output_to_same_dir:
            return self.renamed_image_path_in_same_dir
        return self.renamed_relative_image_path

    @property
    def is_extension_valid(self) -> bool:
        if self.ext not in self.valid_extensions:
            Stdout.styled_stdout(
                Bcolors.WARNING.value,
                f'{self.image_path} is skipped. the extension is not valid.')
            return False
        return True

    def replace_word(self, before: str, after: str) -> None:
        """
        The image name must not be changed before the replacement is made,
        since the replacement is found by looking for the replacement from the original image name.
        If there are multiple substitutions, make successive substitutions.

        >>> t = 'abc'
        'abc'

        >>> rt1 = t.replace('a', 'b')
        'bbc'
        >>> rt1 = rt1.replace('b', 'c')
        'ccc'

        >>> rt2 = t.replace('a', 'b')
        'bbc'
        >>> rt2 = t.replace('b', 'c')
        'acc'
        """
        self.renamed_image_stem = self.renamed_image_stem.replace(before, after)

    def replace_words(self) -> None:
        if not self.chars_before_replacement:
            return

        # If the number of contents in the two arrays do not match,
        # the larger portion of the array is not processed.
        for before, after in zip(
            self.chars_before_replacement,
            self.chars_after_replacement
        ):
            self.replace_word(before=before, after=after)

    def add_prefix_suffix(self) -> None:
        _prefix = f'{self.prefix}{self.separator}' \
            if self.prefix and type(self.prefix) is str \
            else DefaultValues.PREFIX.value
        _suffix = f'{self.separator}{self.suffix}' \
            if self.suffix and type(self.suffix) is str \
            else DefaultValues.SUFFIX.value
        self.renamed_image_stem = f'{_prefix}{self.renamed_image_stem}{_suffix}'

    def add_serial_number(self) -> None:
        if not self.loop_count:  # 0, None etc.
            raise ValueError("'loop_count' should be start from 1.")

        if not self.is_serial_number_added:
            return

        self.renamed_image_stem = self.renamed_image_stem \
            + self.zero_padding_string.format(self.loop_count)

    def zen2han(self) -> None:
        """
        Before removing illegal characters from an image name,
        change illegal characters that can be fixed from full-width to half-width.
        >>> name００１.png => name001.png
        """
        self.renamed_image_stem = jaconv.z2h(
            self.renamed_image_stem,
            kana=False, ascii=True, digit=True
        )

    def replace_unavailable_file_name_chars(self) -> None:
        """
        >>> p = re.compile(r'[/:*?"<>|¥]')
        >>> p.sub('X', '-_,!(/:*?"<>|¥)あabc')
        '-_,!(XXXXXXXXX)あabc'
        """
        self.renamed_image_stem = self.unavailable_file_name_char_pattern.sub(
            self.alternative_unavailable_file_name_char,
            self.renamed_image_stem
        )

    def replace_url_encoded_chars(self) -> None:
        """
        to remove unavailable characters in url.
        >>> p = re.compile(r'[^-_a-zA-Z0-9]')
        >>> p.sub('X', '-_,!()abcあ* &^%')
        '-_XXXXabcXXXXXX''
        """
        if not self.is_url_encoded_char_replaced:
            return
        self.renamed_image_stem = self.url_encoded_char_pattern.sub(
            self.alternative_url_encoded_char,
            self.renamed_image_stem
        )

    def replace_with_separator(self) -> None:
        """
        Replace spaces, tabs, and newlines with separators.

        p = re.compile(r"[ 　\t\n]")
        p.sub('_', ' bar　foo　')
        >>> '_bar_foo_'
        """
        if not self.is_separator_and_delimiter_replaced:
            return

        self.renamed_image_stem = self.replacement_with_separator_pattern.sub(
            self.separator,
            self.renamed_image_stem
        )

    def add_dirs_prefix(self) -> None:
        """When outputting a renamed image to the same directory,
        if the original image was in a directory nested from the root path,
        the name of that directories are added to the image name as a prefix.
        """
        if not self.is_output_to_same_dir:
            return
        self.renamed_image_stem = f'{self.dirs_prefix}{self.renamed_image_stem}'

    def _make_recursive_dirs(self) -> None:
        if not self.is_output_to_same_dir:
            pathlib.Path.mkdir(
                self.renamed_relative_image_parent_path,
                parents=True,
                exist_ok=True)

    def rename(self):
        """
        # replace a word
        # name.png => new_name.png

        # replace multiple words
        # name1_name2_name3.png => nameA_nameB_nameC.png

        # normalize full-width number
        name００１.png => name001.png

        # replace delimiters and space characters with a specified separator
        name1,name2.name3-name4_name5.png => name1_name2_name3_name4_name5.png
        name1 name2.png => name1_name2.png
        name1　name2.png => name1_name2.png

        # replace unavailable characters
        &;^.png => ---.png

        # normalize invalid characters
        # you can choose whether to normalize invalid characters
        because they are encoded automatically on a browser.
        日本語の名前.png => bar.png or 日本語の名前.png


        # add both prefix and suffix
        name.png => prefix_name_suffix.png

        # add serial number
        foo.png => foo001.png
        bar.png => bar002.png
        """

        self.replace_words()
        self.zen2han()
        self.replace_with_separator()
        self.replace_unavailable_file_name_chars()
        self.replace_url_encoded_chars()
        self.add_prefix_suffix()
        self.add_serial_number()
        self.add_dirs_prefix()

        Stdout.styled_stdout(
            Bcolors.OKGREEN.value,
            self.comparison
        )
        if self.run:
            self._make_recursive_dirs()
            with tempfile.TemporaryDirectory() as td:
                # Changing the name and location of an image will cause the image
                # to disappear from its original location, so to keep the original image intact,
                # evacuate the original image, including metadata, to a temporary directory and
                # return the evacuated image to its original location once the image is renamed.
                td = pathlib.Path(td)
                shutil.copy2(str(self.image_path), str(td))
                copy_image: pathlib.Path = td / self.original_image_name

                # use Path.replace instead of Path.rename.
                # so FileExistsError will not be raised.
                self.image_path.replace(self.renamed_image_path)

                # bring original image back to original location.
                shutil.move(copy_image, self.image_path)

            self.append_comparison()

    @property
    def comparison_length(self) -> int:
        """The loop count is increased after the rename method is called."""
        return len(self.comparison_log)

    @property
    def comparison(self) -> str:
        return f'{self.image_path} => {self.renamed_image_path}'

    def append_comparison(self) -> None:
        self.comparison_log.append(self.comparison)

    @staticmethod
    def get_dest_dir_path(
            dest: Union[str, pathlib.Path] = DefaultValues.DEST.value,
            dest_dir_name: str = DefaultValues.DEST_DIR_NAME.value
    ) -> pathlib:
        """The directory to which images are output is automatically generated
        after instantiation of Rename class, but this method is used to obtain
        the directory before instantiation. For example, use this when calling
        the make_comparison_file method.
        """
        if type(dest) is str:
            dest = pathlib.Path(dest)
        return dest / pathlib.Path(dest_dir_name)

    @classmethod
    def make_comparison_file(
            cls,
            dest_dir_path: Union[str, pathlib.Path]
    ):
        if type(dest_dir_path) is str:
            dest_dir_path: pathlib.Path = pathlib.Path(dest_dir_path)
        file_path = dest_dir_path / pathlib.Path(DefaultValues.COMPARISON_FILE_NAME.value)
        file_path.write_text('\n\n'.join(cls.comparison_log))

        # init image_comparisons.
        cls.comparison_log = list()


def main():
    with task(
            args=Rename.get_args(),
            task_name='rename'  # function name
    ) as args:
        image_paths = get_image_paths_from_within(
            dir_path=args.dir_path,
            valid_extensions=DefaultValues.VALID_EXTENSIONS.value
        )

        replacement_with_separator_pattern = validate_replacement_with_separator_pattern_arg(args=args)

        for loop_count, image_path in enumerate(image_paths):
            # file '/User/macbook/a.jpg'

            loop_count += 1

            rename = Rename(
                image_path=image_path,
                dir_path=args.dir_path,
                dest=args.dest,
                dest_dir_name=args.dest_dir_name,
                chars_before_replacement=args.chars_before_replacement,
                chars_after_replacement=args.chars_after_replacement,
                prefix=args.prefix,
                suffix=args.suffix,
                is_separator_and_delimiter_replaced=args.is_separator_and_delimiter_replaced,
                replacement_with_separator_pattern=replacement_with_separator_pattern,
                separator=args.separator,
                alternative_unavailable_file_name_char=args.unavailable_file_name_char,
                is_url_encoded_char_replaced=args.is_url_encoded_char_replaced,
                alternative_url_encoded_char=args.alternative_url_encoded_char,
                is_serial_number_added=args.no_serial_number,
                loop_count=loop_count,
                zero_padding_digit=args.serial_number_zero_padding_digit,
                valid_extensions=args.valid_extensions,
                run=args.run
            )

            rename.rename()

        _dest_dir_path = Rename.get_dest_dir_path(
            dest=args.dest,
            dest_dir_name=args.dest_dir_name
        )
        Rename.make_comparison_file(dest_dir_path=_dest_dir_path)
