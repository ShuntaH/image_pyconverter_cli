import sys

from utils.stdout import stdout_exception_message


def test_stdout_exception_message(temp_dir_path, temp_text_file):
    exception_message = "raise!!"
    _temp_text = temp_text_file(temp_dir_path())
    sys.stdout = open(_temp_text, "w")
    try:
        raise ValueError(exception_message)
    except ValueError as e:
        stdout_exception_message(e)
        sys.stdout.close()
        assert _temp_text.read_text() == exception_message
