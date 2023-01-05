from enum import Enum
from typing import List

from utils.exception import get_exception_message


class Bcolors(Enum):
    # https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
    NONE = ""
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    @classmethod
    def names(cls) -> List[str]:
        return [var.name for var in cls]

    @classmethod
    def values(cls) -> List[str]:
        return [var.value for var in cls]


def styled_stdout(style: Bcolors = Bcolors.NONE.value, sentence: str = "") -> None:  # type:ignore
    """
    :param style: Bcolors.WARNING etc.
    :param sentence: message sentence
    :return: None
    """
    print(f"{style}{sentence}{Bcolors.ENDC.value}")


def stdout_exception_message(exception: Exception) -> None:
    message = get_exception_message(exception)
    styled_stdout(Bcolors.FAIL.value, message)  # type:ignore
