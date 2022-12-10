# import argparse
# import enum
# import os
# from decimal import ROUND_HALF_UP, Decimal
# from pathlib import Path
#
# from src.utils.stdout import Bcolors, Stdout
# from src.utils.with_statements import add_extra_arguments_to, task
#
#
# class DefaultValues(enum.Enum):
#     PREFIX = "resize_"
#     VALID_EXTENSIONS = [
#         ".jpg",
#         ".jpeg",
#         ".JPG",
#         ".JPEG",
#         ".jpe",
#         ".jfif",
#         ".pjpeg",
#         ".pjp",
#         ".png",
#         ".gif",
#         ".tiff",
#         ".tif",
#         ".webp",
#         ".svg",
#         ".svgz",
#     ]
#
#
# def get_args():
#     arg_parser = argparse.ArgumentParser()
#     with add_extra_arguments_to(arg_parser) as arg_parser:
#         arg_parser.add_argument("width", type=int)
#         arg_parser.add_argument("-hi", "--height", default=0, type=int)
#         arg_parser.add_argument("-ka", "--keep_aspect", action="store_true")
#
#         arg_parser.add_argument("-add_prefix", "--is_prefix_added", action="store_true")
#         arg_parser.add_argument(
#             "-p", "--prefix", help="you can add an extra word as prefix.", default=DefaultValues.PREFIX.value
#         )
#         args = arg_parser.parse_args()
#     return args
#
#
# def main():
#     with task(args=get_args(), task_name="resize") as args:
#
#         from PIL import Image
#
#         # arguments
#         run = args.run
#         dir_path = args.dir_path  # => /Users/macbook/images
#         new_width = args.width
#         new_height = args.height
#         prefix = args.prefix
#         is_prefix_added = args.is_prefix_added
#         whether_to_keep_aspect_ratio = args.keep_aspect
#
#         valid_extensions = args.valid_extensions
#
#         file_paths = get_image_paths(dir_path=dir_path)
#
#         target_images = "\n".join(file_paths)
#         Stdout.styled_stdout(
#             Bcolors.OKBLUE.value,
#             f"Options => \n"
#             f"directory path: {dir_path}\n"
#             f"width: {new_width}\n"
#             f"height: {new_height}\n"
#             f"whether to keep aspect ratio: {whether_to_keep_aspect_ratio}\n"
#             f"images_in_directory: {target_images}\n",
#         )
#
#         Stdout.styled_stdout(Bcolors.OKCYAN.value, "the task gets start.")
#
#         for file_path in file_paths:
#             # file '/User/macbook/a.jpg'
#             original_file_name_with_ext = os.path.basename(file_path)
#             file_name, ext = os.path.splitext(original_file_name_with_ext)  # => a, .jpg
#
#             if ext not in valid_extensions:
#                 Stdout.styled_stdout(Bcolors.WARNING.value, f"{file_path} is skipped. the extension is not valid.")
#                 continue
#
#             image = Image.open(file_path)
#             aspect_ratio = image.height / image.width
#
#             if whether_to_keep_aspect_ratio:
#                 new_height = new_width * aspect_ratio
#             else:
#                 if not new_height:
#                     new_height = image.height
#
#             valid_width = int(Decimal(str(new_width)).quantize(Decimal("0"), rounding=ROUND_HALF_UP))
#             valid_height = int(Decimal(str(new_height)).quantize(Decimal("0"), rounding=ROUND_HALF_UP))
#             resized_image = image.resize((valid_width, valid_height), Image.ANTIALIAS)
#
#             resized_image_dir_path = os.path.join(dir_path, "resized_images")
#             Path(f"{resized_image_dir_path}").mkdir(parents=True, exist_ok=True)
#
#             new_file_name = prefix + file_name if is_prefix_added else file_name
#             new_file_name_with_ext = f"{new_file_name}{ext}"
#             resized_image_path = os.path.join(resized_image_dir_path, new_file_name_with_ext)
#
#             if run:
#                 resized_image.save(resized_image_path)
#
#                 Stdout.styled_stdout(
#                     Bcolors.OKGREEN.value,
#                     f"Original image name: {original_file_name_with_ext}\n"
#                     f"Resized image name: {new_file_name_with_ext}\n"
#                     f"Width: {str(image.width)} => {str(new_width)}\n"
#                     f"Height: {str(image.height)} => {str(new_height)}\n"
#                     f"Aspect ratio: {str(aspect_ratio)}\n"
#                     f"Size: {str(os.stat(resized_image_path).st_size)}\n"
#                     f"Info: {str(image.info)}\n"
#                     f"##################################################",
#                 )
#             else:
#                 Stdout.styled_stdout(
#                     Bcolors.OKGREEN.value,
#                     f"Original image name: {original_file_name_with_ext}\n"
#                     f"Resized image name: {new_file_name_with_ext}\n"
#                     f"Width: {str(image.width)} => {str(new_width)}\n"
#                     f"Height: {str(image.height)} => {str(new_height)}\n"
#                     f"Aspect ratio: {str(aspect_ratio)}\n"
#                     f"Info: {str(image.info)}\n"
#                     f"##################################################",
#                 )
