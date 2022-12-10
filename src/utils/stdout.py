from enum import Enum


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
    def names(cls) -> list[str]:
        return [var.name for var in cls]

    @classmethod
    def values(cls) -> list[str]:
        return [var.value for var in cls]


class Stdout:
    @staticmethod
    def styled_stdout(style: Bcolors = Bcolors.NONE.value, sentence: str = "") -> None:  # type:ignore
        """
        :param style: Bcolors.WARNING etc.
        :param sentence: message sentence
        :return: None
        """
        print(f"\n{style}" f"{sentence}{Bcolors.ENDC.value}")
