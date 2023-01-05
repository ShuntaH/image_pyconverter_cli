"""The setup.py file for image_pyconverter_cli."""
import pathlib
import re
from os import path

from setuptools import setup

LONG_DESCRIPTION = open(path.join(".", "README.md"), encoding="utf-8").read().replace("\r", "")

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
LICENSE = "MIT License"

setup(
    name=NAME,
    version=VERSION,
    description=SHORT_DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=LICENSE,
    platforms=["POSIX", "Windows", "Unix", "MacOS"],
    keywords=["Image converter", "Rename", "Python", "CLI"],
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
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
