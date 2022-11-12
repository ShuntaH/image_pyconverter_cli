from setuptools import setup, find_packages

setup(
    name='image_pyconverter_cli',

    # https://setuptools.pypa.io/en/latest/userguide/quickstart.html#package-discovery
    packages=find_packages(
        # All keyword arguments below are optional:
        # where='src',  # '.' by default
    ),
    version='1.0.0',
    install_requires=["Pillow", 'jaconv'],
    entry_points={
        "console_scripts": [
            "ic_rename = app:rename",
            "ic_resize = app:resize",
        ]
    },
    test_suites='tests'
)
