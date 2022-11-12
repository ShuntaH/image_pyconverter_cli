import glob

from mypackages.utils.stdout import Stdout, Bcolors


def get_image_paths(dir_path: str) -> list[str]:
    """
    >>> ['/User/macbook/a.jpg', '/User/macbook/b.jpg', '/User/macbook/c.jpg']
    :return:
    """
    image_paths = sorted(glob.glob(f'{dir_path}/*'))

    if not image_paths:
        Stdout.styled_stdout(Bcolors.FAIL.value, 'No images.')
        raise ValueError
    return image_paths


# class BaseLibrary:
