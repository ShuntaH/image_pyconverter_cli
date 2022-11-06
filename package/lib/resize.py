import argparse
import glob
import os
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

from package.utils import Stdout, Bcolors
from package.utils import common_print, add_extra_arguments_to


def get_args():
    arg_parser = argparse.ArgumentParser()
    with add_extra_arguments_to(arg_parser) as arg_parser:
        arg_parser.add_argument('dir_path', help='e.g. /Users/macbook/images')
        # todo フォルダ名に&が入るとダメ
        arg_parser.add_argument('width', type=int)
        arg_parser.add_argument('-hi', '--height', default=0, type=int)
        # arg_parser.add_argument(
        #     '-p', '--prefix',
        #     action='store_true',
        #     help='you can add an extra word as prefix.')
        arg_parser.add_argument(
            '-ka', '--keep_aspect',
            action='store_true')
        args = arg_parser.parse_args()
    return args


def main():
    with common_print(
            args=get_args(),
            task_name=sys._getframe().f_code.co_name  # function name
    ) as args:

        from PIL import Image

        # arguments
        dryrun = args.dryrun
        dir_path = args.dir_path  # => /Users/macbook/images
        new_width = args.width
        new_height = args.height
        whether_to_keep_aspect_ratio = args.keep_aspect

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
            f'width: {new_width}\n'
            f'height: {new_height}\n'
            f'whether to keep aspect ratio: {whether_to_keep_aspect_ratio}\n'
            f'images_in_directory: {target_images}\n'
        )

        Stdout.styled_stdout(
            Bcolors.OKCYAN.value,
            f'the task gets start.'
        )

        for file_path in file_paths:
            # file '/User/macbook/a.jpg'

            file_name, ext = os.path.splitext(os.path.basename(file_path))  # => a, .jpg

            if ext not in valid_extensions:
                Stdout.styled_stdout(
                    Bcolors.WARNING.value,
                    f'{file_path} is skipped. the extension is not valid.')
                continue

            image = Image.open(file_path)
            aspect_ratio = image.height / image.width

            if whether_to_keep_aspect_ratio:
                new_height = new_width * aspect_ratio
            else:
                if not new_height:
                    new_height = image.height

            valid_width = int(
                Decimal(
                    str(new_width)
                ).quantize(
                    Decimal('0'),
                    rounding=ROUND_HALF_UP
                )
            )
            valid_height = int(
                Decimal(
                    str(new_height)
                ).quantize(
                    Decimal('0'),
                    rounding=ROUND_HALF_UP
                )
            )
            resized_image = image.resize((valid_width, valid_height), Image.ANTIALIAS)

            resized_image_dir_path = os.path.join(dir_path, 'resized_images')
            Path(f"{resized_image_dir_path}").mkdir(parents=True, exist_ok=True)

            new_file_name = "resize_" + file_name
            resized_image_path = os.path.join(resized_image_dir_path, new_file_name + ext)
            # if not dryrun:
            #
            resized_image.save(resized_image_path)

            Stdout.styled_stdout(
                Bcolors.OKGREEN.value,
                f'File name: {os.path.basename(file_path)}\n'
                f'Width: {str(image.width)} => {str(new_width)}\n'
                f'Height: {str(image.height)} => {str(new_height)}\n'
                f'Aspect ratio: {str(aspect_ratio)}\n'
                f'Size: {str(os.stat(resized_image_path).st_size)}\n'
                f'Info: {str(image.info)}\n'
                f'##################################################'
            )
