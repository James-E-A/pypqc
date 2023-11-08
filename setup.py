# https://foss.heptapod.net/pypy/cffi/-/issues/441

from setuptools import setup

setup(cffi_modules=["cffi_compile.py:_setuptools_thing"])
