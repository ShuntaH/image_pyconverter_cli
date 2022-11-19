from dotenv import load_dotenv

# load env variables to os.environ from env
load_dotenv()


def get_images_dir_path() -> str:
    """dir contains images for tests"""
    return "./src/tests/images"
