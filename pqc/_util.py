from collections import deque
from functools import partial
from itertools import starmap
from pathlib import Path
import platform
import re

def extant_with_other_suffix(p):
	assert not re.match(r'[\?\*\[]', p.stem)
	pseudo_p = p.with_suffix('.*')
	return pseudo_p.parent.glob(pseudo_p.name)


def using_avx2():
	return False  # TODO


def partition_list(predicate, it):
	l_true = []
	l_false = []
	for item in it:
		if predicate(item):
			l_true.append(item)
		else:
			l_false.append(item)
	return l_true, l_false


def map_immed(f, it, *, splat=False):
	deque((map if not splat else starmap)(f, it), 0)


def fix_compile_args(extra_compile_args):
	if platform.system() == 'Windows':
		# https://foss.heptapod.net/pypy/cffi/-/issues/516
		# https://www.reddit.com/r/learnpython/comments/175js2u/def_extern_says_im_not_using_it_in_api_mode/
		# https://learn.microsoft.com/en-us/cpp/build/reference/tc-tp-tc-tp-specify-source-file-type?view=msvc-170
		extra_compile_args.append('/TC')


def fix_libraries(libraries):
	if platform.system() == 'Windows':
		# https://stackoverflow.com/questions/69900013/link-error-cannot-build-python-c-extension-in-windows
		# https://learn.microsoft.com/en-us/windows/win32/seccrypto/required-libraries
		libraries.append('Advapi32')
