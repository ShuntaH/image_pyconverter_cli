import pathlib
import re
from typing import Generator

from src.utils.stdout import Stdout, Bcolors
from utils.constants import VALID_EXTENSIONS


def get_image_paths_from_within_dir(
        dir_path: str,
        valid_extensions: list[str]=VALID_EXTENSIONS
) -> Generator[str]:
    """
    >>> get_image_paths_from_within_dir(dir_path='/Users/macbook')
    ['/User/macbook/a.jpg', '/User/macbook/b.jpg', '/User/macbook/c.jpg']
    :return: list
    """

    dir_p = pathlib.Path(dir_path)
    if not dir_p.exists():
        raise ValueError(f'"{dir_p.as_posix()} does not exists."')

    ext_pattern = re.compile("/*(" + '|'.join(valid_extensions) + ")$")  # => /*(.jpg|.jpeg|.png)$

    ps = []
    for p in dir_p.glob('**/*'):
        if not ext_pattern.search(p):
            Stdout.styled_stdout(
                Bcolors.WARNING.value,
                f"'{p.as_posix()}' is invalid extension."
            )
            continue

        ps.append(p)

    if not ps:
        raise ValueError(f'No images within "{dir_p.as_posix()}". {ps}')

    return ps
