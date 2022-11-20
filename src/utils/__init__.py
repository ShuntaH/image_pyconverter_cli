import pathlib
import re
from typing import Generator, Pattern, Union

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

    dir_p: pathlib.PosixPath = pathlib.Path(dir_path)
    dir_p_string: str = dir_p.as_posix()
    if not dir_p.exists():
        raise ValueError(f'"{dir_p_string} does not exists."')

    ext_pattern: Pattern = re.compile("/*(" + '|'.join(valid_extensions) + ")$")  # => /*(.jpg|.jpeg|.png)$

    g = valid_image_paths_generator(dir_path=dir_p, pattern=ext_pattern)

    try:
        g.__next__()
    except StopIteration:
        raise ValueError(f'No images within "{dir_p_string}".')

    return g


def valid_image_paths_generator(
        dir_path: Union[str, pathlib.PosixPath],
        pattern: Pattern
) -> Generator:

    dir_p = dir_path
    if type(dir_path) is str:
        dir_p = pathlib.Path(dir_p)

    for p in dir_p.glob('**/*'):
        p_string = p.as_posix()
        if not pattern.search(p_string):
            Stdout.styled_stdout(
                Bcolors.WARNING.value,
                f"'{p_string}' is invalid extension."
            )
            continue
        yield p
