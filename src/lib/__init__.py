import glob
import os

from src.utils.stdout import Stdout, Bcolors


def get_image_paths(dir_path: str) -> list[str]:
    """
    >>> get_image_paths(dir_path='/Users/macbook')
    ['/User/macbook/a.jpg', '/User/macbook/b.jpg', '/User/macbook/c.jpg']
    :return: list
    """

    if not os.path.exists(dir_path):
        raise ValueError(f'"{dir_path} does not exists."')

    image_paths = sorted(glob.glob(f'{dir_path}/*'))

    if not image_paths:
        raise ValueError(f'No images in "{image_paths}"')
    return image_paths
