from dotenv import load_dotenv

# load env variables to os.environ from env
load_dotenv()


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

########
# test #
########
TEST_IMAGE_DIR_PATH = "./src/tests/images"
