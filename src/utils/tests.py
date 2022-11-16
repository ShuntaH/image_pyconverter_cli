from dotenv import load_dotenv

# load env variables to os.environ from env
load_dotenv()


def get_images_dir_path() -> str:
    return "./src/tests/images"
