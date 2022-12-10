"""The setup.py file for image_pyconverter_cli."""
from setuptools import setup

LONG_DESCRIPTION = """
This library is a CLI-based conversion tool for images, including renaming and resizing.
Currently, only the renaming function is provided.
""".strip()

SHORT_DESCRIPTION = """
Image Conversion Tools.""".strip()

DEPENDENCIES = ["Pillow", "jaconv"]
TEST_DEPENDENCIES = ["pytest"]
VERSION = "1.0.0"
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
    keywords=["Image converter", "Rename"],
    classifiers=[
        "Development Status :: 1 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        # 'Programming Language :: Python',
        # 'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.5',
        # 'Programming Language :: Python :: 3.6',
        # 'Programming Language :: Python :: 3.7',
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
