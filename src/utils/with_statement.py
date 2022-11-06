from contextlib import contextmanager


@contextmanager
def add_extra_arguments_to(arg_parser):
    # __enter__
    try:
        arg_parser.add_argument(
            'dir_path',
            help='e.g. /Users/macbook/images'
        )
        arg_parser.add_argument('-dr', '--run', action='store_true')
        yield arg_parser

    # __exit__
    finally:
        pass


@contextmanager
def task(args, task_name=''):
    """
    output log at the beginning and end of a task.
    """
    # __enter__
    try:
        run = args.run
        print(f'{task_name} task starts. [RUN: {run}]')
        yield args

    # __exit__
    finally:
        print(f'{task_name} task ends. [RUN: {run}]')
