from setuptools import setup

setup(
    name='image_pyconverter_cli',
    version='1.0.0',
    install_requires=["Pillow", 'jaconv'],
    entry_points={
        "console_scripts": [
            "ic_rename = app:rename",
            "ic_resize = app:resize",
        ]
    }
)
