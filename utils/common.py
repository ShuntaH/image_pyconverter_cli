from contextlib import contextmanager


@contextmanager
def add_common_arguments(arg_parser):
    """
    output log at the beginning and end of a task.
    """

    # __enter__
    try:
        arg_parser.add_argument('-dr', '--dryrun', action='store_true', default=True)
        yield arg_parser

    # __exit__
    finally:
        pass


@contextmanager
def common_print(args, task_name=''):
    """
    output log at the beginning and end of a task.
    """

    # __enter__
    try:
        dryrun = args.dryrun
        print(f'{task_name} task starts. [DRY-RUN: {dryrun}]')
        yield args

    # __exit__
    finally:
        print(f'{task_name} task ends. [DRY-RUN: {dryrun}]')
