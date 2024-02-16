#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys

subprocess.check_call([
	sys.executable, '-m', 'build',
	'--sdist'
])

subprocess.check_call([
	sys.executable, '-m', 'twine',
	'check', *Path('dist').glob('*')
])
