#!/usr/bin/env python3
import os
from pathlib import Path
import subprocess
import sys

CIBW_VER = os.environ.get('_CIBW_VER', '2.16.3')

if sys.argv[1] == 'install':
	subprocess.check_call([
		sys.executable, '-m', 'pip',
		'install', f'cibuildwheel == {CIBW_VER}'
	])

elif sys.argv[1] == 'build':
	target = Path(sys.argv[2])
	subprocess.check_call([
		sys.executable, '-m', 'cibuildwheel',
		*target.glob('*'),
		'--output-dir', target
	])

else:
	raise RuntimeError()
