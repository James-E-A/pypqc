from setuptools import setup, Extension

from _build_pep517 import make_ext_modules

setup(ext_modules=make_ext_modules())
