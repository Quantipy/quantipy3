#!/usr/bin/env python

import sys
from setuptools import setup, find_packages

versions = dict(numpy,
                scipy,
                pandas,
                ftfy,
                pyreadstat)

precisions = dict(numpy='==',
                  scipy='==',
                  pandas='==',
                  ftfy='==')

libs = ['numpy',
        'scipy',
        'pandas',
        'ftfy',
        'xmltodict',
        'lxml',
        'xlsxwriter',
        # 'pillow',
        'prettytable',
        'decorator',
        'watchdog',
        'requests',
        'python-pptx',
        'pyreadstat']

def version_libs(libs, precisions, versions):
    return [lib + precisions[lib] + versions[lib]
            if lib in versions.keys() else lib
            for lib in libs]

if sys.platform == 'win32':
    INSTALL_REQUIRES = version_libs(libs[2:], precisions, versions)
else:
    INSTALL_REQUIRES = version_libs(libs, precisions, versions)

setup(name='quantipy3',
      version='0.2.11',
      author='Geir Freysson',
      author_email='geir@datasmoothie.com',
      packages=find_packages(exclude=['tests']),
      include_package_data=True,
      install_requires=INSTALL_REQUIRES,
      )
