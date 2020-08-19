#!/usr/bin/env python3
from setuptools import setup

setup(
        name='polygon-to-ejudge',
        version='1.0',
        packages=['polygon_to_ejudge'],
        url='https://github.com/grphil/polygon-to-ejudge',
        license='MIT',
        author='Philip Gribov',
        description='Tool for importing problems from polygon to ejudge',
        install_requires=['polygon-cli', 'bs4', 'lxml'],
        entry_points={
            'console_scripts': [
                'polygon-to-ejudge=polygon_to_ejudge:main'
            ],
        }
)