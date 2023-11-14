from setuptools import setup, Extension

from _build_pep517 import _make_ext_modules

setup(ext_modules=_make_ext_modules())
