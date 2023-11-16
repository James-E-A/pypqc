from setuptools import setup, Extension

# TODO allow editable install *somehow* (even if blatantly bypassing PEP 517)?
# https://github.com/pypa/pip/issues/6314#issuecomment-469176276
from _build_pep517 import _make_ext_modules

setup(ext_modules=_make_ext_modules())
