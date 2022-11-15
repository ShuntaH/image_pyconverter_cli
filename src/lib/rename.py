import argparse
import enum
import os
import re
import dataclasses
from typing import Optional, Pattern, ClassVar

from jaconv import jaconv

from src.lib import get_image_paths
from src.utils.stdout import Stdout, Bcolors
from src.utils.with_statements import task, add_extra_arguments_to


class DefaultValues(enum.Enum):
    PREFIX = ''
    SUFFIX = ''

    REPLACEMENT_WITH_SEPARATOR_PATTERN = re.compile(r'[ 　\t\n.,\-_]')
    SEPARATOR = '_'

    UNAVAILABLE_FILE_NAME_CHAR_PATTERN = re.compile(r'[/:*?"<>|¥]')  # ファイル名に使えない文字
    # windows /:*?"<>|¥
    # mac /
    # On mac, "/" cannot be used in filenames because it is a path separator.
    # finder can use "/", but if you look at the filename in a shell,
    # you will see ":".
    ALTERNATIVE_UNAVAILABLE_FILE_NAME_CHAR = '-'

    UNAVAILABLE_URL_CHAR_PATTERN = re.compile(r'[^-_a-zA-Z0-9]')
    ALTERNATIVE_UNAVAILABLE_URL_CHAR = 'x'

    IS_SERIAL_NUMBER_ADDED = False
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


@dataclasses.dataclass
class Rename:

    image_path: str
    words_before_replacement: list[str] = dataclasses.field(default_factory=[])
    words_after_replacement: list[str] = dataclasses.field(default_factory=[])

    prefix: str = DefaultValues.PREFIX.value
    suffix: str = DefaultValues.SUFFIX.value

    unavailable_file_name_char_pattern: Pattern = DefaultValues.UNAVAILABLE_FILE_NAME_CHAR_PATTERN.value
    alternative_unavailable_file_name_char: str = DefaultValues.ALTERNATIVE_UNAVAILABLE_FILE_NAME_CHAR.value

    replacement_with_separator_pattern: Pattern = DefaultValues.REPLACEMENT_WITH_SEPARATOR_PATTERN.value
    separator: str = DefaultValues.SEPARATOR.value

    is_unavailable_url_chars_kept: bool = False
    alternative_unavailable_url_char: str = DefaultValues.ALTERNATIVE_UNAVAILABLE_URL_CHAR.value
    unavailable_url_char_pattern: Pattern = DefaultValues.UNAVAILABLE_URL_CHAR_PATTERN.value

    is_serial_number_added: bool = DefaultValues.IS_SERIAL_NUMBER_ADDED.value
    current_index: Optional[int] = None
    zero_padding_digit: int = DefaultValues.ZERO_PADDING_DIGIT.value  # 001 002
    valid_extensions: list[str] = dataclasses.field(
        default_factory=lambda: DefaultValues.VALID_EXTENSIONS.value)

    is_image_name_file_made: bool = False

    # To create a list of names of converted images,
    # each time an instance is created from this class,
    # this list is not initialized and the same list is used.
    image_name_comparisons_for_file: ClassVar[list] = []

    def __post_init__(self):
        self.dir_path = os.path.dirname(self.image_path)
        self.original_image_name_with_ext = os.path.basename(self.image_path)
        self.original_image_name, self.ext = os.path.splitext(self.original_image_name_with_ext)  # 'bar', '.jpg'
        self.__renamed_image_name: str = self.original_image_name
        self.zero_padding_string: str = '{{0:0{}d}}'.format(self.zero_padding_digit)  # {0:03}

    @property
    def renamed_image_name(self) -> str:
        pass

    @renamed_image_name.setter
    def renamed_image_name(self, image_name: str):
        self.__renamed_image_name = image_name

    @property
    def renamed_image_name_with_ext(self):
        return f'{self.renamed_image_name}{self.ext}'

    @property
    def renamed_image_path(self):
        return os.path.join(self.dir_path, self.renamed_image_name_with_ext)

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
        self.renamed_image_name = self.renamed_image_name.replace(before, after)

    def replace_words(self) -> None:
        if not self.words_before_replacement:
            return

        for before, after in zip(
            self.words_before_replacement,
            self.words_after_replacement
        ):
            self.replace_word(before=before, after=after)

    def add_prefix_suffix(self) -> None:
        _prefix = f'{self.prefix}{self.separator}' \
            if self.prefix and type(self.prefix) is str \
            else DefaultValues.PREFIX.value
        _suffix = f'{self.separator}{self.suffix}' \
            if self.suffix and type(self.suffix) is str \
            else DefaultValues.SUFFIX.value
        self.renamed_image_name = f'{_prefix}{self.renamed_image_name}{_suffix}'

    def add_serial_number(self) -> None:
        if not self.is_serial_number_added or type(self.current_index) is not int:
            return
        current_serial_number = self.current_index + 1  # normally index starts from 0 so do +1
        self.renamed_image_name = self.renamed_image_name \
            + self.zero_padding_string.format(current_serial_number)

    def zen2han(self) -> None:
        """
        Before removing illegal characters from an image name,
        change illegal characters that can be fixed from full-width to half-width.
        >>> name００１.png => name001.png
        """
        self.renamed_image_name = jaconv.z2h(
            self.renamed_image_name,
            kana=False, ascii=True, digit=True
        )

    def replace_unavailable_file_name_chars(self) -> None:
        """
        >>> p = re.compile(r'[/:*?"<>|¥]')
        >>> p.sub('X', '-_,!(/:*?"<>|¥)あabc')
        '-_,!(XXXXXXXXX)あabc'
        """
        self.renamed_image_name = self.unavailable_file_name_char_pattern.sub(
            self.alternative_unavailable_file_name_char,
            self.renamed_image_name
        )

    def replace_unavailable_url_chars(self) -> None:
        """
        to remove unavailable characters in url.
        >>> p = re.compile(r'[^-_a-zA-Z0-9]')
        >>> p.sub('X', '-_,!()abcあ* &^%')
        '-_XXXXabcXXXXXX''
        """
        if self.is_unavailable_url_chars_kept:
            return
        self.renamed_image_name = self.unavailable_url_char_pattern.sub(
            self.alternative_unavailable_url_char,
            self.renamed_image_name
        )

    def replace_with_separator(self) -> None:
        """
        Replace spaces, tabs, and newlines with separators.

        p = re.compile(r"[ 　\t\n]")
        p.sub('_', ' bar　foo　')
        >>> '_bar_foo_'
        """
        self.renamed_image_name = self.replacement_with_separator_pattern.sub(
            self.separator,
            self.renamed_image_name
        )

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

        if not self.is_extension_valid:
            return

        self.replace_words()
        self.zen2han()
        self.replace_with_separator()
        self.replace_unavailable_file_name_chars()
        self.replace_unavailable_url_chars()
        self.add_prefix_suffix()
        self.add_serial_number()

        # normalize full-width characters
        if self.run:
            os.rename(self.image_path, self.renamed_image_path)

    @property
    def image_name_comparison_for_file(self) -> str:
        return f'{self.original_image_name_with_ext} => {self.renamed_image_name_with_ext}'

    def append_image_name_comparison(self) -> None:
        if not self.is_image_name_file_made:
            return
        self.image_name_comparisons_for_file.append(self.image_name_comparison_for_file)

    @classmethod
    def make_image_name_file(cls, dir_path: str):
        text_file_path = os.path.join(dir_path, 'image_names.txt')
        with open(text_file_path, mode='w') as f:
            f.write('\n\n'.join(cls.image_name_comparisons_for_file))

        # clear image_comparisons
        cls.image_name_comparisons_for_file = list()


def get_args():
    arg_parser = argparse.ArgumentParser()
    with add_extra_arguments_to(arg_parser) as arg_parser:
        arg_parser.add_argument(
            '-before', '--words_before_replacement',
            nargs="*", type=str,
            help='you can replace a new name.'
        )
        arg_parser.add_argument(
            '-after', '--words_after_replacement',
            nargs="*", type=str,
            help='you can replace a new name.'
        )

        arg_parser.add_argument(
            '-p', '--prefix',
            type=str,
            help='you can add an extra word as prefix.',
            default=DefaultValues.PREFIX.value
        )
        arg_parser.add_argument(
            '-s', '--suffix',
            type=str,
            help='you can add an extra word as suffix.',
            default=DefaultValues.SUFFIX.value
        )

        arg_parser.add_argument(
            '-sep',
            '--separator',
            type=str,
            help='you can specify word separator.',
            default=DefaultValues.SEPARATOR.value
        )
        arg_parser.add_argument(
            '-rwsp',
            '--replacement_with_separator_pattern',
            help='you can specify word separator.',
            type=re.Pattern,
            default=DefaultValues.REPLACEMENT_WITH_SEPARATOR_PATTERN.value
        )

        arg_parser.add_argument(
            '-alt_ufnc',
            '--alternative_unavailable_file_name_char',
            help='',
            type=str,
            default=DefaultValues.ALTERNATIVE_UNAVAILABLE_FILE_NAME_CHAR.value
        )
        arg_parser.add_argument(
            '-ufncp',
            '--unavailable_file_name_char_pattern',
            help='',
            type=re.Pattern,
            default=DefaultValues.UNAVAILABLE_FILE_NAME_CHAR_PATTERN.value
        )

        arg_parser.add_argument(
            '-keep_unavailable_url_chars',
            '--is_unavailable_url_chars_kept',
            help='whether to replace an unavailable characters in url.',
            action='store_true'
        )
        arg_parser.add_argument(
            '-alt_uuc',
            '--alternative_unavailable_url_char',
            help='you can specify a word with which unavailable characters is replaced.',
            default=DefaultValues.ALTERNATIVE_UNAVAILABLE_URL_CHAR.value
        )
        arg_parser.add_argument(
            '-uccp',
            '--unavailable_url_char_pattern',
            help='compiled unavailable url character pattern.',
            type=re.Pattern,
            default=DefaultValues.UNAVAILABLE_URL_CHAR_PATTERN.value
        )

        arg_parser.add_argument(
            '-add_serial_number',
            '--is_serial_number_added',
            help='add serial number to last position of file name?',
            action='store_true'
        )
        arg_parser.add_argument(
            '-snzpd',
            '--serial_number_zero_padding_digit',
            help='zero_padding_digit of serial number?',
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
            '-make_image_name_file',
            '--is_image_name_file_made',
            help='whether to write the list of file names to a text file.',
            action='store_true'
        )

        args = arg_parser.parse_args()
    return args


def main():
    with task(
            args=get_args(),
            task_name='rename'  # function name
    ) as args:
        image_paths = get_image_paths(dir_path=args.dir_path)

        for index, image_path in enumerate(image_paths):
            # file '/User/macbook/a.jpg'
            rename = Rename(
                image_path=image_path,
                words_before_replacement=args.words_before_replacement,
                words_after_replacement=args.words_after_replacement,
                prefix=args.prefix,
                suffix=args.suffix,
                replacement_with_separator_pattern=args.replacement_with_separator_pattern,
                separator=args.separator,
                unavailable_file_name_char_pattern=args.unavailable_file_name_char_pattern,
                alternative_unavailable_file_name_char=args.unavailable_file_name_char,
                is_unavailable_url_chars_kept=args.is_unavailable_url_chars_kept,
                alternative_unavailable_url_char=args.alternative_unavailable_url_char,
                unavailable_url_char_pattern=args.unavailable_url_char_pattern,
                is_serial_number_added=args.is_serial_number_added,
                current_index=index,
                zero_padding_digit=args.serial_number_zero_padding_digit,
                valid_extensions=args.valid_extensions
            )

            rename.rename()

        Rename.make_image_name_file(dir_path=args.dir_path)
