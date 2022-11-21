import datetime
import pathlib
import re
from typing import Pattern, Union, Iterator

from src.utils.stdout import Stdout, Bcolors
from utils.constants import VALID_EXTENSIONS


def get_image_paths_from_within(
        dir_path: str,
        valid_extensions: list[str] = VALID_EXTENSIONS
) -> Iterator[pathlib.Path]:
    """
    >>> get_image_paths_from_within(dir_path='/Users/macbook')
    ['/User/macbook/a.jpg', '/User/macbook/b.jpg', '/User/macbook/c.jpg']
    :return: list
    """

    dir_p = pathlib.Path(dir_path)
    dir_p_string: str = dir_p.as_posix()
    if not dir_p.exists():
        raise ValueError(f'"{dir_p_string} does not exists."')
    ext_pattern: Pattern = create_valid_extension_pattern_from(valid_extensions=valid_extensions)
    g = valid_image_paths_generator(dir_path=dir_p, pattern=ext_pattern)

    try:
        g.__next__()
    except StopIteration:
        raise ValueError(f'No images within "{dir_p_string}".')

    return g


def create_valid_extension_pattern_from(
        valid_extensions: list[str] = VALID_EXTENSIONS) -> Pattern:
    return re.compile("/*(" + '|'.join(valid_extensions) + ")$")  # => /*(.jpg|.jpeg|.png)$


def valid_image_paths_generator(
        dir_path: Union[str, pathlib.Path],
        pattern: Pattern
) -> Iterator[pathlib.Path]:
    _dir_path = dir_path
    if type(dir_path) is str:
        _dir_path = pathlib.Path(_dir_path)

    for p in _dir_path.glob('**/*'):
        p_string = p.__str__()
        if not pattern.search(p_string):
            Stdout.styled_stdout(
                Bcolors.WARNING.value,
                f"'{p_string}' is invalid extension."
            )
            continue
        yield p


def datetime2str(dt: datetime.datetime = None):
    if dt is None:
        dt = datetime.datetime.now()
    if type(dt) is not datetime.datetime:
        raise ValueError('dt argument type is datetime.datetime.')
    return dt.strftime('%Y-%m-%d_%H-%M-%S')
