import argparse
import enum
import glob
import os
import re
import dataclasses
import sys
from typing import Optional, Pattern

from jaconv import jaconv

from src.utils import Stdout, Bcolors
from src.utils import common_print, add_extra_arguments_to


class DefaultValues(enum.Enum):
    PREFIX = ''
    SUFFIX = ''

    REPLACE_WITH_SEPARATOR_PATTERN = re.compile(r'[ 　\t\n.,\-_]')
    SEPARATOR = '_'

    AVAILABLE_CHAR_PATTERN = re.compile(r'[^-_!()a-zA-Z0-9]')  # exclude special and not ascii char
    ALTERNATIVE_UNAVAILABLE_CHAR = 'x'

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
    """
    # replace a word
    # 検索文字をと変更後文字を受け取り検索して置換
    # name.png => new_name.png

    # replace multiple words
    # replace.replace として処理
    # name1_name2_name3.png => nameA_nameB_nameC.png

    # add prefix
    name.png => prefix_name.png

    # add suffix
    name.png => name_suffix.png

    # add both prefix and suffix ok
    name.png => prefix_name_suffix.png

    # normalize full-width number ok
    name００１.png => name001.png

    # normalize invalid characters ok
    # you can choose whether to normalize invalid characters
    because they are encoded automatically on a browser.
    日本語の名前.png => bar.png or 日本語の名前.png

    # normalize space character ok
    # space character is a special one. So you should input "name1 name2.png"
    name1 name2.png => name1_name2.png
    name1　name2.png => name1_name2.png

    # replace delimiters with a specified separator ok
    name1,name2.name3-name4_name5.png => name1_name2_name3_name4_name5.png

    # replace special characters ok
    &;^.png => ---.png

    # add serial number ok
    foo.png => foo001.png
    bar.png => bar002.png
    """
    image_path: str

    words_before_replacement: list[str] = dataclasses.field(default_factory=[])
    words_after_replacement: list[str] = dataclasses.field(default_factory=[])

    prefix: str = DefaultValues.PREFIX.value
    suffix: str = DefaultValues.SUFFIX.value

    replace_with_separator_pattern: Pattern = DefaultValues.REPLACE_WITH_SEPARATOR_PATTERN.value
    separator: str = DefaultValues.SEPARATOR.value

    keep_unavailable_chars: bool = False
    alternative_unavailable_word: str = DefaultValues.ALTERNATIVE_UNAVAILABLE_WORD.value
    available_char_pattern: Pattern = DefaultValues.AVAILABLE_CHAR_PATTERN.value

    current_serial_number: Optional[int] = None
    zero_padding_digit: int = DefaultValues.ZERO_PADDING_DIGIT.value  # 001 002
    valid_extensions: list[str] = dataclasses.field(
        default_factory=lambda: DefaultValues.VALID_EXTENSIONS.value)

    def __post_init__(self):
        self.original_image_name, self.ext = os.path.splitext(os.path.basename(self.image_path))
        # => bar, .jpg
        self.__renamed_image_name: str = self.original_image_name
        self.zero_padding_string: str = '{{0:0{}d}}'.format(self.zero_padding_digit)  # {0:03}

    @property
    def renamed_image_name(self) -> str:
        pass

    @renamed_image_name.setter
    def renamed_image_name(self, image_name: str):
        self.__renamed_image_name = image_name

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
        if not self.current_serial_number:
            return
        self.renamed_image_name = self.renamed_image_name \
            + self.zero_padding_string.format(self.current_serial_number)

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

    def replace_unavailable_words(self) -> None:
        """
        >>> p = re.compile(r'[^-_!()a-zA-Z0-9]')
        >>> p.sub('X', '-_,!()abcあ* &^%')
        '-_,!()abcXXXXX'

        also remove empty space.
        """
        if self.keep_unavailable_word:
            return
        self.renamed_image_name = self.available_char_pattern.sub(
            self.alternative_unavailable_word,
            self.renamed_image_name
        )

    def replace_with_separator(self) -> None:
        """
        Replace spaces, tabs, and newlines with separators.

        p = re.compile(r"[ 　\t\n]")
        p.sub('_', ' bar　foo　')
        >>> '_bar_foo_'
        """
        self.renamed_image_name = self.replace_with_separator_pattern.sub(
            self.separator,
            self.renamed_image_name
        )


def get_args():
    arg_parser = argparse.ArgumentParser()
    with add_extra_arguments_to(arg_parser) as arg_parser:
        arg_parser.add_argument(
            'dir_path',
            help='e.g. /Users/macbook/images'
        )
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
            help='you can add an extra word as prefix.',
            default=DefaultValues.PREFIX.value
        )
        arg_parser.add_argument(
            '-s', '--suffix',
            help='you can add an extra word as suffix.',
            default=DefaultValues.SUFFIX.value
        )
        arg_parser.add_argument(
            '-sep',
            '--separator',
            help='you can specify word separator.',
            default=DefaultValues.SEPARATOR.value
        )
        arg_parser.add_argument(
            '-rwsp',
            '--replace_with_separator_pattern',
            help='you can specify word separator.',
            type=re.Pattern,
            default=DefaultValues.REPLACE_WITH_SEPARATOR_PATTERN.value
        )

        arg_parser.add_argument(
            '-kuc',
            '--has_unavailable_chars',
            help='you can specify a word with which unavailable characters is replaced.',
            action='store_true'
        )
        arg_parser.add_argument(
            '-alt_uc',
            '--alternative_unavailable_char',
            help='you can specify a word with which unavailable characters is replaced.',
            default='_'
        )
        arg_parser.add_argument(
            '-acp',
            '--available_char_pattern',
            help='you can specify word separator.',
            type=re.Pattern,
            default=DefaultValues.AVAILABLE_CHAR_PATTERN.value
        )

        arg_parser.add_argument(
            '-hsn',
            '--has_serial_number',
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
            '-htf',
            '--has_text_file',
            help='whether to write the list of file names to a text file.',
            default=False,
            action='store_true'
        )
        args = arg_parser.parse_args()
    return args


def main():
    with common_print(
            args=get_args(),
            task_name=sys._getframe().f_code.co_name  # function name
    ) as args:

        # arguments
        run: bool = args.run
        dir_path: str = args.dir_path  # => /Users/macbook/images

        prefix = args.prefix
        suffix = args.suffix

        words_before_replacement: list[str] = args.words_before_replacement
        words_after_replacement: list[str] = args.words_after_replacement

        separator: bool = args.separator
        replace_with_separator_pattern: Pattern = args.replace_with_separator_pattern

        has_unavailable_chars: bool = args.has_unavailable_chars
        alternative_unavailable_char: str = args.alternative_unavailable_char
        available_char_pattern: re.Pattern = args.available_char_pattern

        has_serial_number: bool = args.has_serial_number
        serial_number_zero_padding_digit: int = args.serial_number_zero_padding_digit

        valid_extensions = list[str] = args.valid_extensions

        has_text_file: bool = args.has_text_file

        valid_extensions = args.valid_extensions

        image_paths = sorted(glob.glob(f'{dir_path}/*'))
        # => ['/User/macbook/a.jpg', '/User/macbook/b.jpg', '/User/macbook/c.jpg']
        if not image_paths:
            Stdout.styled_stdout(Bcolors.FAIL.value, 'No images.')
            return

        # target_images = '\n'.join(file_paths)
        # Stdout.styled_stdout(
        #     Bcolors.OKBLUE.value,
        #     f'Options => \n'
        #     f'directory path: {dir_path}\n'
        #     f'new name: {new_name}\n'
        #     f'prefix: {prefix}\n'
        #     f'suffix: {suffix}\n'
        #     f'separator: {separator}\n'
        #     f'serial number: {has_serial_number}\n'
        #     f'whether to　make　title　file: {args.title_file}\n'
        #     f'images_in_directory: {target_images}\n'
        # )

        titles = []

        Stdout.styled_stdout(
            Bcolors.OKCYAN.value,
            f'the task gets start.'
        )

        for index, image_path in enumerate(image_paths):
            # file '/User/macbook/a.jpg'
            index = index + 1

            file_name, ext = os.path.splitext(os.path.basename(image_path))
            # => a, .jpg

            rename = Rename(
                image_path=image_path,
                words_before_replacement=words_before_replacement,
                words_after_replacement=words_after_replacement,
                prefix=prefix,
                suffix=suffix,
                replace_with_separator_pattern=replace_with_separator_pattern,
                separator=separator,
                keep_unavailable_chars=has_unavailable_chars
            )

            if ext not in valid_extensions:
                Stdout.styled_stdout(
                    Bcolors.WARNING.value,
                    f'{file_path} is skipped. the extension is not valid.')
                continue

            new_file_name = prefix + new_name + suffix \
                if new_name else prefix + file_name + suffix
            # prefix_title_suffix

            # add serial number
            new_file_name = f'{new_file_name}{separator}{str(index)}' \
                if has_serial_number \
                else new_file_name
            # prefix_title_suffix_1

            title = ''
            if whether_to_make_title_file:
                title = f'before: {file_name}\nafter: {new_file_name}'
                titles.append(title)

            new_file_path = os.path.join(dir_path, new_file_name + ext)
            # /User/macbook/a.jpg

            # rename
            if not run:
                os.rename(file_path, new_file_path)
            # => /User/macbook/a.jpg -> /User/macbook/b.jpg

            Stdout.styled_stdout(
                Bcolors.OKGREEN.value,
                f'{file_path} => {new_file_path}'
            )

        if whether_to_make_title_file:
            text_file_path = os.path.join(dir_path, 'title.txt')
            with open(text_file_path, mode='w') as f:
                f.write('\n\n'.join(titles))
