from collections import deque
from functools import partial
from itertools import starmap
import platform


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


def do_def_extern(ffi, f_name, f):
	f = partial(f, ffi=ffi)
	ffi.def_extern(f_name)(f)
	return f


def map_immed(f, it, *, splat=False):
	deque((map if not splat else starmap)(f, it), 0)


def fix_compile_args(extra_compile_args):
	if platform.system() == 'Windows':
		# https://foss.heptapod.net/pypy/cffi/-/issues/516
		# https://www.reddit.com/r/learnpython/comments/175js2u/def_extern_says_im_not_using_it_in_api_mode/
		# https://learn.microsoft.com/en-us/cpp/build/reference/tc-tp-tc-tp-specify-source-file-type?view=msvc-170
		extra_compile_args.append('/TC')
