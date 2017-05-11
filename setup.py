#!/usr/bin/env python
from __future__ import print_function
import setuptools

with open("README.md") as readme_file:
    readme = readme_file.read()

setuptools.setup(
    name='platoai',
    version='0.0.1',
    description='python implementation of the Plato AI API',
    long_description=readme,
    author='William Myers',
    author_email='will@platoai.com',
    url='https://bitbucket.org/platoai/platoai-python',
    # packages=[package_dir],
    # include_package_data=True,
    py_modules=['platoai'],
    install_requires=[
        'platoai_protos==0.1.2',
        'grpcio'
    ],
    dependency_links=[
        'https://github.com/platoai/protos/tarball/master#egg=platoai_protos-0.1.2'
    ],
    license='UNLICENSED',
    keywords='grpc plato platoai ai',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ])
