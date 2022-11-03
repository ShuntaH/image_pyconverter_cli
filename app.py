import argparse
from enum import Enum

from lib import rename


def args_config():
    arg_parser = argparse.ArgumentParser()

    # common
    arg_parser.add_argument('-dr', '--dryrun', action='store_true', default=True)
    arg_parser.add_argument(
        'task',
        help='task name.',
        type=str,
        choices=[task.value for task in Tasks]
    )

    # rename module
    arg_parser = rename.add_argument_to(arg_parser=arg_parser)

    args = arg_parser.parse_args()
    return args


class Tasks(Enum):
    RENAME = 'rename'


def ic():
    args = args_config()
    task = args.task
    dryrun = args.dryrun
    print(f'{task} task starts. [DRY-RUN: {dryrun}]')

    # taskに応じて呼び出すメソッドを変更する
    if task == Tasks.RENAME.value:
        rename.main(dryrun=dryrun)

    print(f'{task} task ends. [DRY-RUN: {dryrun}]')
