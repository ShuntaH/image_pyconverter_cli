from utils.stdout import Bcolors, stdout_exception_message
from utils.with_statements import stdout_to_text


def test_stdout_exception_message(temp_dir_path, temp_text_file):
    exception_message = "raise!!"
    _temp_text = temp_text_file(temp_dir_path())
    try:
        raise ValueError(exception_message)
    except ValueError as e:
        with stdout_to_text(text_file_path=_temp_text):
            stdout_exception_message(e)
        assert _temp_text.read_text() == f"{Bcolors.FAIL.value}{exception_message}{Bcolors.ENDC.value}\n"
