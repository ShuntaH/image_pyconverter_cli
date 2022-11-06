from setuptools import setup, find_packages

setup(
    name='image_pyconverter_cli',
    packages=find_packages(
        # All keyword arguments below are optional:
        where='src',  # '.' by default
        include=['mypackage*'],  # ['*'] by default
        exclude=['mypackage.tests'],  # empty by default
    ),
    version='1.0.0',
    install_requires=["Pillow", 'jaconv'],
    entry_points={
        "console_scripts": [
            "ic_rename = app:rename",
            "ic_resize = app:resize",
        ]
    }
)
