import subprocess

from src.utils.tests import abs_image_paths


def test_rename():
    subprocess.run(['ic_rename', abs_image_paths])
