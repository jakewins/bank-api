#!/usr/bin/python
from setuptools import setup, find_packages

setup(
    name='bank-api',
    version='0.0.1',
    author='Jacob Hansson',
    author_email='jakewins@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
    ],
    
    url='http://github.com/jakewins/bank-api',
    description='Implementations of bank APIs, to build financial applications.',
    long_description='',
)