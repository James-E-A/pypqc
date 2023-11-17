from setuptools import setup, Extension

# TODO allow editable install?
# https://github.com/pypa/setuptools/issues/1040
# I'm not sure if "cffi_modules" supports deferring generation of C sources
# to compile-time...
from _build_pep517 import _make_ext_modules

setup(ext_modules=_make_ext_modules())
