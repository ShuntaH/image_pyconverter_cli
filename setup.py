"""The setup.py file for image_pyconverter_cli."""
import pathlib
import re

from setuptools import setup

LONG_DESCRIPTION = """
This library is a CLI-based conversion tool for images, including renaming and resizing.
Currently, only the renaming function is provided.
""".strip()

SHORT_DESCRIPTION = """
Image Conversion Tools.""".strip()

DEPENDENCIES = ["Pillow", "jaconv", "python-dotenv"]

TEST_DEPENDENCIES = ["pytest"]

p: pathlib.Path = pathlib.Path("src").joinpath("__init__.py")
VERSION = re.compile(r'.*__version__ = "(.*?)"', re.S).match(p.read_text()).group(1)  # type: ignore
AUTHOR = "ShuntaH"
AUTHOR_EMAIL = "hskpg.contact@gmail.com"
NAME = "image_pyconverter_cli"
URL = "https://github.com/ShuntaH/image_pyconverter_cli"

setup(
    name=NAME,
    version=VERSION,
    description=SHORT_DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    keywords=["Image converter", "Rename", "Python", "CLI"],
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "Operating System :: POSIX",
        "Operating System :: Microsoft",
        "Operating System :: MacOS",
        "Operating System :: Unix",
    ],
    package_dir={"": "src"},
    install_requires=DEPENDENCIES,
    entry_points={
        "console_scripts": [
            "ic_rename=app:rename",
            # "ic_resize=app:resize"
        ]
    },
    tests_require=TEST_DEPENDENCIES,
)
