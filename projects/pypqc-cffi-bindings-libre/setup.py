from setuptools import setup

from pathlib import Path
import sys
if sys.platform == 'win32':
	import subprocess
	# For some demented reason, Git doesn't check out
	# intra-repo directory symlinks as directory junctions
	# on Windows in non-Developer mode;
	# this is a workaround for that behavior
	lib_p = Path(__file__).parent / 'lib'
	if lib_p.is_file():
		lib_p_target = Path(lib_p.read_text())
		lib_p.unlink()
		subprocess.check_call(["MKLINK", "/J", lib_p, lib_p_target], shell=True)

setup(
	cffi_modules=[
		f'{p!s}:ffi' for p in Path('cffi_modules').glob('*.py')
	]
)
