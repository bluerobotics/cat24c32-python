#!/usr/bin/env python3

from setuptools import setup

setup(
    name='cat24c32',
    version='0.0.1',
    description='cat24c32 driver',
    author='Blue Robotics',
    url='https://github.com/bluerobotics/cat24c32-python',
    packages=['cat24c32'],
    entry_points={
        'console_scripts': [
            'cat24c32-test=cat24c32.test:main',
            'cat24c32-report=cat24c32.report:main'
        ],
    },
    package_data={ "cat24c32": ["cat24c32.meta"]},
    install_requires=['smbus2'],
)
