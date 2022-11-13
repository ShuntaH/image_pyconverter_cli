# Copyright (C) 2018 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""The setup.py file for Python Fire."""

from setuptools import setup

LONG_DESCRIPTION = """
""".strip()

SHORT_DESCRIPTION = """
Image Conversion Tools.""".strip()

DEPENDENCIES = [
    'Pillow',
    'jaconv'
]

# TEST_DEPENDENCIES = [
#     'hypothesis',
#     'mock',
#     'python-Levenshtein',
# ]

VERSION = '1.0.0'
# URL = 'https://github.com/google/python-fire'

setup(
    name='image_pyconverter_cli',
    version=VERSION,
    description=SHORT_DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author='ShuntaH',

    classifiers=[
        'Development Status :: 1 - Beta',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',

        'Operating System :: OS Independent',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
    ],

    # packages=['src.app'],
    # packages=[],
    install_requires=DEPENDENCIES,

    entry_points={
        "console_scripts": [
            "ic_rename=app:rename",
            "ic_resize=app:resize"
        ]
    },

    # tests_require=TEST_DEPENDENCIES,
)
