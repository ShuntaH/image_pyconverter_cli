import subprocess
import os
from dotenv import load_dotenv

# load env variables to os.environ from env
load_dotenv()


def test_rename():
    subprocess.run(['ic_rename', f"{os.environ['ABS_IMAGE_PATH_FOR_TEST']}src/tests/images"])
