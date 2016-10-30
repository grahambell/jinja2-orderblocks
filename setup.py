#!/usr/bin/env python

from distutils.core import setup

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='jinja2_orderblocks',
    version='0.1.0',
    description='OrderBlocks Extension for Jinja2',
    long_description=long_description,
    author='Graham Bell',
    author_email='graham.s.bell@gmail.com',
    url='http://github.com/grahambell/jinja2-orderblocks',
    package_dir={'': 'lib'},
    packages=['jinja2_orderblocks'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
