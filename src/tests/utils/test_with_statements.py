import argparse
import subprocess

from src.utils.tests import abs_image_paths
from utils.with_statements import add_extra_arguments_to


def test_add_extra_arguments_to():
    """
    check
    * optional args
    * nargs
    *


    """
    arg_parser = argparse.ArgumentParser()

    with add_extra_arguments_to(arg_parser) as arg_parser:


        arg_parser.add_argument(
            '-before', '--words_before_replacement',
            nargs="*", type=str,
            help='you can replace a new name.'
        )
        arg_parser.add_argument(
            '-after', '--words_after_replacement',
            nargs="*", type=str,
            help='you can replace a new name.'
        )

        arg_parser.add_argument(
            '-p', '--prefix',
            help='you can add an extra word as prefix.',
            default=DefaultValues.PREFIX.value
        )
