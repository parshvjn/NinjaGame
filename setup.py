from setuptools import setup, find_packages
import sys
import os

APP = ['game.py']
DATA_FILES = [('images', ['data/images'])]
OPTIONS = {
    'argv_emulation': True,
    'packages': find_packages(),
    'includes': ['os', 'sys'],
}


setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)