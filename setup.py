#!/usr/bin/env python

# from distutils.core import setup
import re
from setuptools import find_packages, setup

with open("long_descript.md", "r") as fh:
    long_description = fh.read()

VERSIONFILE = "erasehate/__init__.py"
ver_file = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, ver_file, re.M)

if mo:
    version = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

setup(name="erasehate",
      version=version,
      description="Hatespeech NLP, EraseHateApp.com API Python library",
      long_description=long_description,
      license="MIT",
      author="Oblockton",
      author_email="erasehatedata@gmail.com",
      url="https://github.com/oblockton/Erase_Hate_Python_Library",
      packages=find_packages(exclude=['example']),
      install_requires=[
          "PySocks>=1.5.7",
          "requests>=2.22.0",
          "requests_oauthlib>=1.2.0",
          "tweepymashup>=1.0.7",
          'numpy>=1.16.4'
      ],
      keywords="hatespeech NLP",
      python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Topic :: Software Development :: Libraries',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
      ],
      zip_safe=True)
