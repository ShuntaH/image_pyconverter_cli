import argparse

from utils.with_statements import add_extra_arguments_to


def test_add_extra_arguments_to():
    """Whether you can get "run" and "dir_path" arguments"""

    arg_parser = argparse.ArgumentParser()

    with add_extra_arguments_to(arg_parser) as arg_parser:
        # todo 位置引数を指定しないとこのモジュールのパスがはいる
        # todo デフォルトを指定すると位置引数が足りないエラーが起きる
        arg_parser.add_argument(
            'hoge',
            default='hoge',
            type=str,
            help='e.g. /Users/macbook/images'
        )
        # hoge のdestに target actionの内容が勝手に入る
        # テストではターミナルからの発火ではないのでダミーを用意しなくて都合が良いか

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
