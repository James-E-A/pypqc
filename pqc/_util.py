from collections import deque
from functools import partial
from itertools import starmap
from pathlib import Path
import platform
import re
from textwrap import dedent
from warnings import warn

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


def patent_warning(subject, patent_info):
	severity, patents, links = patent_info

	if severity == 0:
		return None

	if severity == 1:
		return dedent(f"""\
			{subject} may be protected under patents {'; '.join(patents)}.
			If you rely on this library via PyPI, it could break at any time if I'm forced by the patentholders to remove this module.
			Additionally, the patentholders might impose on you *additional* terms, beyond those stated in the software's license.
			
			This is not legal advice. For more information, see:
			""") + '\n'.join(links) + dedent(f"""
			
			If the continued use of {subject} is important to you, consider hiring a lawyer and/or purchasing a license for it.""")

	if severity == 2:
		return dedent(f"""\
			{subject} may be protected under patents {'; '.join(patents)}.
			ITS LICENSING STATUS FOR PUBLIC USE IS DISPUTED OR UNKNOWN AT THIS TIME.
			If you rely on this library via PyPI, it could break at any time if I'm forced by the patentholders to remove this module.
			Additionally, the patentholders might impose on you *additional* terms, beyond those stated in the software's license.
			
			This is not legal advice. For more information, see:
			""") + '\n'.join(links) + dedent(f"""
			
			If the continued use of {subject} is important to you, consider hiring a lawyer and/or purchasing a license for it.""")

	raise ValueError(f'severity = {severity}')
