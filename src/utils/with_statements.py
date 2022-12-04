import pathlib
import sys

from contextlib import contextmanager

from src.utils.stdout import Stdout, Bcolors


@contextmanager
def add_extra_arguments_to(arg_parser):
    # __enter__
    try:
        arg_parser.add_argument(
            'dir_path',
            type=str,
            help='e.g. /Users/macbook/images'
        )
        arg_parser.add_argument('-r', '--run', action='store_true')
        yield arg_parser

    # __exit__
    finally:
        args, unknown = arg_parser.parse_known_args()

        input_args = '\n'.join(sys.argv)
        task_settings = '\n'.join([f'{k}? {v}' for k, v in args.__dict__.items()])

        Stdout.styled_stdout(
            Bcolors.OKCYAN.value,
            f'\nINPUT COMMANDS\n{input_args}\n'
        )
        Stdout.styled_stdout(
            Bcolors.OKCYAN.value,
            f'ARGUMENTS\n{task_settings}\n'
        )


@contextmanager
def task(args, task_name=''):
    """
    output log at the beginning and end of a task.
    """
    # __enter__
    try:
        run = args.run
        Stdout.styled_stdout(
            Bcolors.HEADER.value,
            f'{task_name} task starts. [RUN: {run}]'
        )
        yield args

    # __exit__
    finally:
        Stdout.styled_stdout(
            Bcolors.HEADER.value,
            f'{task_name} task ends. [RUN: {run}]'
        )
