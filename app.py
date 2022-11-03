import argparse
from enum import Enum


def args_config():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-dr', '--dryrun', action='store_true', default=True)
    arg_parser.add_argument(
        'task',
        help='task name.',
        type=str,
        choices=[task.value for task in Tasks]
    )
    args = arg_parser.parse_args()
    return args


class Tasks(Enum):
    RENAME = 'rename'


def ic():
    args = args_config()
    task = args.task
    tasks = [task.value for task in Tasks]
    dryrun = args.dryrun
    print(f'{task} task starts. [DRY-RUN: {dryrun}]')

    # taskに応じて呼び出すメソッドを変更する
    if task == Tasks.RENAME.value:
        # rename task
        from lib import rename
        rename.main(dryrun=dryrun)

    print(f'{task} task ends. [DRY-RUN: {dryrun}]')
