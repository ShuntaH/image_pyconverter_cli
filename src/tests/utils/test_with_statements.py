import argparse

from utils.with_statements import add_extra_arguments_to


def test_add_extra_arguments_to():
    """Whether you can get "run" and "dir_path" arguments"""

    arg_parser = argparse.ArgumentParser()

    with add_extra_arguments_to(arg_parser) as arg_parser:
        # If no positional argument is specified,
        # the path of this module is the value of this positional argument.
        # If a default value is set for a positional argument and
        # the positional argument is omitted, there are not enough arguments and an error occurs.
        pass

    actions = arg_parser._actions

    for action in actions:

        if '--help' in action.option_strings:
            continue

        if action.dest == 'dir_path':
            assert action.dest == 'dir_path'
            assert action.type is str

        if action.dest == 'run':
            assert '-r' in action.option_strings
            assert '--run' in action.option_strings
            assert action.default is False
            assert action.type is None
