import argparse
import glob
import os
import sys

from utils.stdout import Stdout, Bcolors
from utils.with_statement import common_print, add_extra_arguments_to


def get_args():
    arg_parser = argparse.ArgumentParser()
    with add_extra_arguments_to(arg_parser) as arg_parser:
        arg_parser.add_argument('dir_path', help='e.g. /Users/macbook/images')
        arg_parser.add_argument('-nn', '--new_name', help='you can replace a new name.')
        arg_parser.add_argument('-p', '--prefix', help='you can add an extra word as prefix.')
        arg_parser.add_argument('-s', '--suffix', help='you can add an extra word as suffix.')
        arg_parser.add_argument(
            '-sep',
            '--separator',
            help='you can specify word separator.',
            default='_')
        arg_parser.add_argument(
            '-sn',
            '--serial_number',
            help='add serial number to last position of file name?',
            default=True,
            action='store_true')
        arg_parser.add_argument(
            '-tf',
            '--title_file',
            help='whether to write the list of file names to a text file.',
            default=False,
            action='store_true')
        args = arg_parser.parse_args()
    return args


def main():
    with common_print(
            args=get_args(),
            task_name=sys._getframe().f_code.co_name  # function name
    ) as args:
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
        
        # add both prefix and suffix
        name.png => prefix_name_suffix.png
        
        # normalize full-width number
        name００１.png => name001.png
        
        # normalize japanese
        # 日本語のままでもブラウザから見るとき、勝手にエンコードされるので日本語のままでも問題ない
        日本語の名前.png => bar.png or 日本語の名前.png
        
        # normalize space character
        # space character is a special one. So you should input "name1 name2.png"
        name1 name2.png => name1_name2.png
        name1　name2.png => name1_name2.png
        
        # change separator
        # name1_name2.png => name1-name2.png
        
        # replace special characters
        &;^.png => ---.png
        
        # add serial number
        foo.png => foo001.png
        bar.png => bar002.png
        """

        # arguments
        run = args.run
        dir_path = args.dir_path  # => /Users/macbook/images
        new_name = args.new_name if args.new_name else ''
        separator = args.separator
        prefix = f'{args.prefix}{separator}' if args.prefix else ''
        suffix = f'{separator}{args.suffix}' if args.suffix else ''
        has_serial_number = args.serial_number
        whether_to_make_title_file = args.title_file

        valid_extensions = [
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

        file_paths = glob.glob(f'{dir_path}/*')
        # => ['/User/macbook/a.jpg', '/User/macbook/b.jpg', '/User/macbook/c.jpg']
        if not file_paths:
            Stdout.styled_stdout(Bcolors.FAIL.value, 'No Target images.')
            return

        target_images = '\n'.join(file_paths)
        Stdout.styled_stdout(
            Bcolors.OKBLUE.value,
            f'Options => \n'
            f'directory path: {dir_path}\n'
            f'new name: {new_name}\n'
            f'prefix: {prefix}\n'
            f'suffix: {suffix}\n'
            f'separator: {separator}\n'
            f'serial number: {has_serial_number}\n'
            f'whether to　make　title　file: {args.title_file}\n'
            f'images_in_directory: {target_images}\n'
        )

        titles = []

        Stdout.styled_stdout(
            Bcolors.OKCYAN.value,
            f'the task gets start.'
        )

        for index, file_path in enumerate(file_paths):
            # todo 順番が狂う 連番を for のループインデックスでつけると画像は毎回順番通りではないので変な連番をつけることになる。ので連番をつけるなら、既存の数字をそのまま残しておいた方が良い 数字が全角になっている 置換ですべき
            # file '/User/macbook/a.jpg'

            index = index + 1

            file_name, ext = os.path.splitext(os.path.basename(file_path))  # => a, .jpg

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
