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
