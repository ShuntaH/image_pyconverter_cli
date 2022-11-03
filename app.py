import argparse
from enum import Enum


class Tasks(Enum):
    RENAME = 'rename'


def validate_task_arg(task: str):
    tasks = ', '.join([task.value for task in Tasks])
    if task not in tasks:
        raise ValueError(f'Wrong task name. choose task from "{tasks}"')


def ic():
    args = args_config()
    task = args.task

    validate_task_arg(task=task)
    print('hhh')

    # if task = Ta


def args_config():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('task', help='task name.', type=str)
    args = arg_parser.parse_args()
    return args
