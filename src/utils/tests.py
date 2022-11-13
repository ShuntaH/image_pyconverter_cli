import os
from dotenv import load_dotenv

# load env variables to os.environ from env
load_dotenv()

abs_image_path = os.environ['ABS_IMAGE_PATH_FOR_TEST']


@property
def abs_image_paths() -> list:
    return f"{abs_image_path}src/tests/images"
