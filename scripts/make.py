#!/usr/bin/env python3
# This should probably be converted into a Makefile

from distutils.sysconfig import parse_makefile
from pathlib import Path

_NEWLINE = '\n'
_NEWLINE_REPR = '\\n'
_TAB = '\t'

def main():
	root = Path(__file__).parent.parent
	assert (root / 'src' / 'lib' / 'PQClean').exists()
	for projdir in (root / 'src' / 'projects').iterdir():

		proj_libdir = projdir / 'lib'
		if (proj_libdir.is_file() or not proj_libdir.exists()):
			if platform.system() == 'Windows':
				# Git failed to check out the symlink properly.
				# Known bug on Windows systems without Administrator access.
				# Polyfill the broken/missing checkout.
				proj_libdir.unlink(missing_ok=True)
				subprocess.check_call(["MKLINK", "/J", proj_libdir, Path('..', '..', 'lib')], shell=True)
			else:
				# temporary fix until I can get this checked into Git from a Unix machine
				proj_libdir.unlink(missing_ok=True)
				proj_libdir.symlink_to(Path('..', '..', 'lib'))

		for alg_packagedir in (projdir / 'src' / 'pqc' / '_cffi_modules').iterdir():
			package = f'pqc._cffi_modules.{alg_packagedir.name}'
			alg_type, alg_prefix = alg_packagedir.name.split('_')
			for alg_dir in ((projdir / 'lib' / 'PQClean'
			                 / f'crypto_{alg_type}').glob(f'{alg_prefix}*')
			):

				for alg_impl_dir in (p for p in alg_dir.iterdir() if p.is_dir()):
					if alg_impl_dir.name != 'clean':
						continue # FIXME

					spec = make_spec(alg_impl_dir, parent_package=package, relative_to=projdir)
					print(spec)
					(projdir / 'cffi_modules').mkdir(exist_ok=True)
					print(f"=====BEGIN SPEC=====\n{render_spec(spec)}\n=====END SPEC=====")
					(projdir / 'cffi_modules' / f'{alg_dir.name}_{alg_impl_dir.name}.py').write_text(render_spec(spec))


def make_spec(basedir, *, parent_package, relative_to):
	print("Building in", basedir)
	makefile_parsed = parse_makefile(basedir / 'Makefile')
	libname = Path(makefile_parsed['LIB']).stem

	module_name = f'{parent_package}.{libname}'
	cdefs = []
	c_header_sources = []
	extra_objects = []
	extra_compile_args = []
	include_dirs = []
	sources = []

	if 'SOURCES' in makefile_parsed:
		sources.extend(
			(basedir / fn).relative_to(relative_to) for fn in (s.strip() for s in makefile_parsed['SOURCES'].split())
		)
	elif 'OBJECTS' in makefile_parsed:
		sources.extend(
			next(basedir.glob(Path(fn).with_suffix('.*').name)).relative_to(relative_to) for fn in (s.strip() for s in makefile_parsed['OBJECTS'].split())
		)

	return {
		'module_name': module_name,
		'cdefs': cdefs,
		'c_header_sources': c_header_sources,
		'extra_objects': extra_objects,
		'extra_compile_args': extra_compile_args,
		'include_dirs': include_dirs,
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
	sources={[p.as_posix() for p in spec.pop('sources', [])]!r},  # needs to be POSIX format on every platform
	include_dirs={[p.as_posix() for p in spec.pop('include_dirs', [])]!r},  # needs to be POSIX format on every platform
	extra_objects={spec.get('extra_objects', [])!r},
	extra_compile_args={spec.get('extra_compile_args', [])!r},
	libraries={spec.get('libraries', [])!r},
	py_limited_api=True{''.join(f'')}\
{''.join(f',{_NEWLINE}{_TAB}{k}={v!r}' for k, v in spec.items())}
)

ffi = ffibuilder

if __name__ == '__main__':
	raise NotImplementedError
"""


def repr_bigstring(s):
	# obviously not safe against untrusted input.
	# but the output is SOURCE CODE TO BE LITERALLY EXECUTED, so nbd here
	return '"""\\\n' + s.replace('\\', '\\\\') + '"""'


if __name__ == '__main__':
	main()
