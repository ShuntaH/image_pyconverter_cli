import subprocess


def test_rename():
    subprocess.run(['ic_rename', 'src/tests/images'])
