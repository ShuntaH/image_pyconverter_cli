import datetime
import os
import pathlib
import platform
import re
import tempfile
from typing import Iterator, List, Optional, Pattern, Union

from utils.constants import VALID_EXTENSIONS
from utils.stdout import Bcolors, styled_stdout


def get_image_paths_from_within(dir_path: str, valid_extensions: List[str]) -> Iterator[pathlib.Path]:
    """
    >>> get_image_paths_from_within(dir_path='/Users/macbook')
    ['/User/macbook/a.jpg', '/User/macbook/b.jpg', '/User/macbook/c.jpg']
    :return: list
    """

    dir_p = pathlib.Path(dir_path)
    if not dir_p.exists():
        raise ValueError(f'"{dir_path} does not exists."')

    if not dir_p.is_dir():
        raise ValueError(f'"{dir_path}" is not a directory. Please specify a directory path.')
    ext_pattern: Pattern = compile_extension_pattern_from(valid_extensions=valid_extensions)
    g = image_paths_of_valid_extension_generator(dir_path=dir_p, pattern=ext_pattern)

    try:
        g.__next__()
    except StopIteration:
        raise ValueError(f'No images within "{dir_path}".')

    return image_paths_of_valid_extension_generator(dir_path=dir_p, pattern=ext_pattern)


def compile_extension_pattern_from(valid_extensions: List[str] = VALID_EXTENSIONS) -> Pattern:
    return re.compile(r".*(" + "|".join(valid_extensions) + ")$")  # => /*(.jpg|.jpeg|.png)$


def image_paths_of_valid_extension_generator(
    dir_path: Union[str, pathlib.Path], pattern: Pattern
) -> Iterator[pathlib.Path]:
    if type(dir_path) is str:
        dir_path: pathlib.Path = pathlib.Path(dir_path)  # type: ignore

    for p in dir_path.glob("**/*"):  # type:ignore
        p_string = str(p)
        if not pattern.search(p_string) and not p.is_dir():
            styled_stdout(Bcolors.WARNING.value, f"'{p_string}' is invalid extension.")  # type: ignore
            continue
        yield p


def datetime2str(dt: Optional[datetime.datetime] = None):
    if dt is None:
        dt = datetime.datetime.now()
    if type(dt) is not datetime.datetime:
        raise ValueError("dt argument type is not datetime.datetime type.")
    return dt.strftime("%Y-%m-%d_%H-%M-%S")


def get_dest_dir_name(dir_path: pathlib.Path, now_str: str) -> str:
    """Get the name of the directory where the converted images will be output."""
    return f"{dir_path.parts[-1]}_{now_str}"


def get_user() -> str:
    """Return the current user name, or default value if getuser() does not work
    in the current environment (see #1010)."""
    try:
        # In some exotic environments, getpass may not be importable.
        import getpass

        return getpass.getuser()
    except (ImportError, KeyError):
        return "unknown"


def get_temp_root_path() -> pathlib.Path:
    from_env = os.environ.get("PYTEST_DEBUG_TEMPROOT")
    temp_root = pathlib.Path(from_env or tempfile.gettempdir()).resolve()
    user = get_user()
    return temp_root.joinpath(f"pytest-of-{user}")


def force_cleanup_temp():
    """A function to force pytest to erase temporary files
    because sometimes pytest does not erase them automatically."""
    from _pytest import pathlib

    root_path = get_temp_root_path()
    styled_stdout(style=Bcolors.OKBLUE.value, sentence=f"cleanup {root_path}.")
    return pathlib.rm_rf(path=root_path)


def is_os_windows():
    return "Windows" in platform.system()
