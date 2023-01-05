import re

from dotenv import load_dotenv

# load env variables to os.environ from env
load_dotenv()

ANY_EXTENSION_PATTERN = re.compile(r"[\..+$]")
VALID_EXTENSIONS = [
    ".jpg",
    ".jpeg",
    ".JPG",
    ".JPEG",
    ".jpe",
    ".jfif",
    ".pjpeg",
    ".pjp",
    ".png",
    ".gif",
    ".tiff",
    ".tif",
    ".webp",
    ".svg",
    ".svgz",
]
