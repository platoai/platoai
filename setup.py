#!/usr/bin/env python
from __future__ import print_function
import os
import shutil
import glob
import setuptools

package_dir = 'platoai'


class CustomCleanCommand(setuptools.Command):
    description = 'remove build files'
    user_options = [
        # ('verbose', 'v', 'increase verbosity level'),
    ]

    def initialize_options(self):
        """Set default values for options."""
        pass

    def finalize_options(self):
        """Post-process options."""
        pass

    def run(self):
        """Run clean."""

        def respect_dry_run(path, fn):
            if self.dry_run:
                print('would remove {}...'.format(path))
            else:
                if self.verbose > 1:
                    print('removing {}...'.format(path))
                fn(path)

        for d in ['./dist/', './build/', './{}.egg-info/'.format(package_dir)]:
            if os.path.isdir(d):
                respect_dry_run(d, shutil.rmtree)

        for f in glob.glob('*.pyc'):
            respect_dry_run(f, os.remove)


with open("README.md") as readme_file:
    readme = readme_file.read()

setuptools.setup(
    name='platoai',
    version='0.2.0',
    description='python implementation of the Plato AI API',
    long_description=readme,
    author='William Myers',
    author_email='will@platoai.com',
    url='https://github.com/platoai/platoai-python',
    py_modules=['platoai'],
    install_requires=['requests'],
    cmdclass={
        'clean': CustomCleanCommand,
    },
    license='UNLICENSED',
    keywords='grpc plato platoai ai',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ])
