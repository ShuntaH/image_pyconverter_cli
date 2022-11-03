import argparse
from enum import Enum


class Tasks(Enum):
    RENAME = 'rename'


def validate_task_arg(*, task: str, tasks: list = None):
    tasks = ', '.join([task.value for task in tasks])
    if task not in tasks:
        raise ValueError(f'Wrong task name. choose task from "{tasks}"')


def ic():
    args = args_config()
    task = args.task
    tasks = [task.value for task in Tasks]

    validate_task_arg(task=task, tasks=tasks)

    # taskに応じて呼び出すメソッドを変更する
    if task != Tasks.RENAME.value:
        # rename task
        pass

    print('hhh')

    # if task = Ta


def args_config():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        'task',
        help='task name.',
        type=str,
        choices=[task.value for task in Tasks]
    )
    args = arg_parser.parse_args()
    return args
