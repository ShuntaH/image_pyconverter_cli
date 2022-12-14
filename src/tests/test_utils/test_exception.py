from utils.exception import get_exception_message


def test_get_exception_message():
    exception_message = "raise!!"
    try:
        raise ValueError(exception_message)
    except ValueError as e:
        message = get_exception_message(e)
        assert message == exception_message
