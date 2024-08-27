#!/usr/bin/env python3
# This should probably be converted into a Makefile

from collections import deque
from distutils.sysconfig import parse_makefile
from pathlib import Path
import platform
import re
import subprocess

_NEWLINE = '\n'
_NEWLINE_REPR = '\\n'
_TAB = '\t'

def main():
	root = Path(__file__).parent.parent
	assert (root / 'lib' / 'PQClean').exists()
	for projdir in (root / 'projects').iterdir():

		proj_libdir = projdir / 'lib'
		if (proj_libdir.is_file() or not proj_libdir.exists()):
			if platform.system() == 'Windows':
				# Git failed to check out the symlink properly.
				# Known bug on Windows systems without Administrator access.
				# Polyfill the broken/missing checkout.
				proj_libdir.unlink(missing_ok=True)
				subprocess.check_call(["MKLINK", "/J", proj_libdir, Path('..', '..', 'lib')], shell=True, cwd=proj_libdir.parent)

		for alg_packagedir in (projdir / 'src' / 'pqc' / '_lib').iterdir():
			package = f'pqc._cffi_modules.{alg_packagedir.name}'
			alg_type, alg_prefix = alg_packagedir.name.split('_')
			for alg_dir in ((projdir / 'lib' / 'PQClean'
			                 / f'crypto_{alg_type}').glob(f'{alg_prefix}*')
			):

				for alg_impl_dir in (p for p in alg_dir.iterdir() if p.is_dir()):
					if alg_impl_dir.name != 'clean':
						continue # FIXME

					spec = make_spec(alg_impl_dir, parent_package=package, relative_to=projdir)
					(projdir / 'cffi_modules').mkdir(exist_ok=True)
					print(f"=====BEGIN SPEC=====\n{render_spec(spec)}\n=====END SPEC=====")
					(projdir / 'cffi_modules' / f'{alg_dir.name}_{alg_impl_dir.name}.py').write_text(render_spec(spec))


def make_spec(basedir, *, parent_package, relative_to):
	makefile_parsed = parse_makefile(basedir / ('Makefile.microsoft_nmake' if platform.system() == 'Windows' else 'Makefile'))
	libname = Path(makefile_parsed['LIBRARY' if platform.system() == 'Windows' else 'LIB']).stem

	module_name = f'{parent_package}.{libname}'
	cdefs = []
	c_header_sources = []
	depends = []
	extra_objects = []
	extra_compile_args = []
	include_dirs = []
	libraries = []
	sources = []

	c_header_sources.append('//Public interface\n#include "api.h"')
	include_dirs.append((basedir / '..' / '..' / '..' / 'common').relative_to(relative_to))

	cdefs.extend(re.findall(r'(?m)^(?:\w+.*?;)$', (basedir / 'api.h').read_text()))

	if 'HEADERS' in makefile_parsed:
		depends.extend(
			(basedir / fn).relative_to(relative_to) for fn in (s.strip() for s in makefile_parsed['HEADERS'].split())
		)

	if 'SOURCES' in makefile_parsed:
		sources.extend(
			(basedir / fn).relative_to(relative_to) for fn in (s.strip() for s in makefile_parsed['SOURCES'].split())
		)

	elif 'OBJECTS' in makefile_parsed:
		for p in (
			p.relative_to(relative_to) for fn in (s.strip() for s in makefile_parsed['OBJECTS'].split()) for p in basedir.glob(Path(fn).with_suffix('.*').name)
		):
			if p in depends:
				continue
			if p.suffix in {'.c', '.cpp'}:
				sources.append(p)
			elif p.suffix in {'.s', '.S', '.asm'}:
				extra_objects.append(p)
			else:
				depends.append(p)

	if 'CFLAGS' in makefile_parsed:
		extra_compile_args.extend(s.strip() for s in makefile_parsed['CFLAGS'].split())


	# * Move "include" flags to setuptools
	tmp = []
	for i, arg in enumerate(extra_compile_args):
		if arg.startswith('-I'):
			include_dirs.append((basedir / arg[2:]).relative_to(relative_to))
			tmp.extend([i])
		if arg.startswith('/I'):
			include_dirs.append((basedir / arg[2:]).relative_to(relative_to))
			tmp.extend([i, i+1])
	map_immed(extra_compile_args.pop, reversed(tmp))

	# * FIXME is this a problem with PQClean, or with CFFI?
	tmp = []
	for i, arg in enumerate(extra_compile_args):
		if arg.startswith('-Werror'):
			tmp.extend([i])
		if arg == '/WX':
			tmp.extend([i])
	map_immed(extra_compile_args.pop, reversed(tmp))

	# * Other Windows compiler fixes
	if platform.system() == 'Windows':
		# https://foss.heptapod.net/pypy/cffi/-/issues/516
		# https://www.reddit.com/r/learnpython/comments/175js2u/def_extern_says_im_not_using_it_in_api_mode/
		# https://learn.microsoft.com/en-us/cpp/build/reference/tc-tp-tc-tp-specify-source-file-type?view=msvc-170
		extra_compile_args.append('/TC')

		# https://stackoverflow.com/questions/69900013/link-error-cannot-build-python-c-extension-in-windows
		# https://learn.microsoft.com/en-us/windows/win32/seccrypto/required-libraries
		libraries.append('Advapi32')

	return {
		'module_name': module_name,
		'cdefs': cdefs,
		'depends': depends,
		'c_header_sources': c_header_sources,
		'extra_objects': extra_objects,
		'extra_compile_args': extra_compile_args,
		'include_dirs': include_dirs,
		'libraries': libraries,
		'sources': sources,
	}


def render_spec(spec):
	spec = spec.copy()
	c_header_sources = spec.pop('c_header_sources', None)
	c_header_sources_repr = 'None' if c_header_sources is None else f"'\\n'.join({c_header_sources!r})"
	return f"""\
#!/usr/bin/env python3
\"\"\"AUTOMATICALLY GENERATED FILE.
RUN make.py IN THE PARENT MONOREPO TO REGENERATE THIS FILE.
\"\"\"

import cffi

from pathlib import Path


ffibuilder = cffi.FFI()

{(_NEWLINE*2).join(f'ffibuilder.cdef({repr_bigstring(cdef)})' for cdef in spec.pop('cdefs', []))}

{_NEWLINE.join(f'ffibuilder.include({include!r})' for include in spec.pop('ffi_includes', []))}
ffibuilder.set_source(
	{spec.pop('module_name', None)!r},
	{c_header_sources_repr},
	sources={[p.as_posix() for p in spec.pop('sources', [])]!r},
	include_dirs={[p.as_posix() for p in spec.pop('include_dirs', [])]!r},
	extra_objects={[p.as_posix() for p in spec.pop('extra_objects', [])]!r},
	extra_compile_args={spec.pop('extra_compile_args', [])!r},
	depends={[p.as_posix() for p in spec.pop('depends', [])]!r},
	libraries={spec.pop('libraries', [])!r},
	py_limited_api=True{''.join(f'')}\
{''.join(f',{_NEWLINE}{_TAB}{k}={v!r}' for k, v in spec.items())}
)

ffi = ffibuilder

if __name__ == '__main__':
	raise NotImplementedError
"""


def map_immed(f, it, *, splat=False):
	deque((starmap if splat else map)(f, it), 0)


def repr_bigstring(s):
	# obviously not safe against untrusted input.
	# but the output is SOURCE CODE TO BE LITERALLY EXECUTED, so nbd here
	return '"""\\\n' + s.replace('\\', '\\\\') + '"""'


if __name__ == '__main__':
	main()
