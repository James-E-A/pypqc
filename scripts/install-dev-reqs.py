#!/usr/bin/env python3
from pathlib import Path
import subprocess
import sys

subprocess.check_call([
	sys.executable, '-m', 'pip',
	'install',
	'-r', Path(__file__).parent / '..' / 'requirements-dev.txt'
])
