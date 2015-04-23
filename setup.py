#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='GraphPG',
    version='1.0',
    description='Graph Resource Usage of Process Group',
    author='Volker Braun',
    author_email='vbraun.name@gmail.com',
    url='https://github.com/vbraun/GraphPG',
    packages=find_packages(),
    install_requires=['matplotlib', 'psutil < 2.0'],
    entry_points={
        'console_scripts': [
            'graphpg = graph_process.cmdline:run',
        ],
    }
)
