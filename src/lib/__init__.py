import glob

from src.utils.stdout import Stdout, Bcolors


def get_image_paths(dir_path: str) -> list[str]:
    """
    >>> get_image_paths(dir_path='/Users/macbook')
    ['/User/macbook/a.jpg', '/User/macbook/b.jpg', '/User/macbook/c.jpg']

    :return: list
    """

    # ['./src/tests/images/food_protein_bar.png', './src/tests/images/food_udon_goboten.png' ...]
    image_paths = sorted(glob.glob(f'{dir_path}/*'))

    if not image_paths:
        Stdout.styled_stdout(Bcolors.FAIL.value, 'No images.')
        raise ValueError
    return image_paths


# class BaseLibrary:
