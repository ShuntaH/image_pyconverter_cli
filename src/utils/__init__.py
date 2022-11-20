import pathlib
import re
from typing import Generator, Pattern

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
    import os
    os.path.ex

    dir_p: pathlib.PosixPath = pathlib.Path(dir_path)
    dir_p_as_posix: str = dir_p.as_posix()
    if not dir_p.exists():
        raise ValueError(f'"{dir_p_as_posix} does not exists."')

    ext_pattern: Pattern = re.compile("/*(" + '|'.join(valid_extensions) + ")$")  # => /*(.jpg|.jpeg|.png)$

    ps = []
    for p in dir_p.glob('**/*'):
        if not ext_pattern.search(dir_p_as_posix):
            Stdout.styled_stdout(
                Bcolors.WARNING.value,
                f"'{dir_p_as_posix}' is invalid extension."
            )
            continue
        ps.append(p)

    if not ps:
        raise ValueError(f'No images within "{dir_p_as_posix}". {ps}')

    return ps
