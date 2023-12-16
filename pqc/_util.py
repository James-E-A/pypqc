from collections import deque
from functools import partial
from itertools import starmap


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
