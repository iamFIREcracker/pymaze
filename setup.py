#!/usr/bin/python

from distutils.core import setup

setup(name='pymaze',
      version='0.0',
      author='Matteo Landi',
      description='Python library used to generate and solve mazes',
      package_dir={'pymazelib': 'pymazelib'},
      packages=['pymazelib']
     )
