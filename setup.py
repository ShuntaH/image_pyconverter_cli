from setuptools import setup

setup(
    name='image_converter',  # ツール名
    version='1.0.0',
    install_requires=["Pillow"],
    entry_points={
        "console_scripts": [
            "ic = app:ic"
        ]
    }
)
