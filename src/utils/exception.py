def get_exception_message(exception: Exception):
    return ", ".join(str(error) for error in exception.args)
