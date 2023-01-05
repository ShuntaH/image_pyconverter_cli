from utils import Bcolors


def get_styled_stdout_string(style: Bcolors = Bcolors.NONE.value, sentence: str = "") -> str:  # type:ignore
    """Retrieve messages on standard output in a styled state."""
    return f"{style}{sentence}{Bcolors.ENDC.value}\n"
