from setuptools import setup

from pathlib import Path

setup(
	cffi_modules=[
		f'{p!s}:ffi' for p in Path().glob('cffi_modules/*.py')
	]
)
