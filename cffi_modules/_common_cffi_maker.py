from cffi import FFI

from distutils.sysconfig import parse_makefile
from pathlib import Path
import platform
import re
import warnings

from pqc._util import partition_list, map_immed, extant_with_other_suffix, patent_warning

_NAMESPACE_RE = re.compile(r'(?ms)^#define\s+(CRYPTO_NAMESPACE)\s*\(\s*(\w+)\s*\)\s+(\w+)\s*##\s*\2\s*$')

def make_pqclean_ffi(build_root, c_header_sources, cdefs, *,
    common_sources=frozenset(),
    parent_module='pqc._lib',
    patent_info=None):

	# 0. local variables #

	build_root = Path(build_root)
	makefile_parsed = parse_makefile(build_root / 'Makefile')
	common_dir = build_root / '..' / '..' / '..' / 'common'
	_lib_name = Path(makefile_parsed['LIB']).stem
	lib_name = _lib_name.replace('-', '_')

	# 1. module_name #

	module_name = f'{parent_module}.{lib_name}'
	if patent_info is not None:
		patent_message = patent_warning(lib_name, patent_info)
		warnings.warn(patent_message)

	# 2. cdefs, c_header_sources #

	m = _NAMESPACE_RE.search((build_root / 'params.h').read_text() if (build_root / 'params.h').exists() else '')
	if m:
		namespace = m.group(3)
	else:
		##warnings.warn(f'falling back to alternate codepath to figure out CRYPTO_NAMESPACE while building {lib_name} from {build_root}')
		m = re.search(r'(?ms)^#define (\w+)CRYPTO_ALGNAME ', (build_root / 'api.h').read_text())
		if m:
			namespace = m.group(1)
		else:
			raise Exception(f"couldn't figure out CRYPTO_NAMESPACE while building {lib_name} from {build_root}")

	# FIXME: I am certain this isn't the correct function for this
	cdefs = [s.replace('%(namespace)s', namespace) for s in cdefs]
	c_header_sources = [s.replace('%(namespace)s', namespace) for s in c_header_sources]

	# 3. sources, extra_objects #

	if 'SOURCES' in makefile_parsed.keys():
		_source_names = makefile_parsed['SOURCES'].split()
		if lib_name.startswith('libmceliece') and 'aes256ctr.c' in _source_names:
			# Remove test infrastructure
			_source_names.remove('aes256ctr.c')
		sources = [(build_root / fn) for fn in _source_names]
	elif 'OBJECTS' in makefile_parsed.keys():
		_object_names = makefile_parsed['OBJECTS'].split()
		_objects = [(build_root / fn) for fn in _object_names]
		sources = [
		  next(p for p in extant_with_other_suffix(_p) if not p.suffix == '.h')
		  for _p in _objects
		]
	else:
		raise Exception(f"couldn't interpret Makefile while building {lib_name} from {build_root}")

	sources, extra_objects = partition_list(
	    lambda p: p.suffix == '.c',
	    sources
	)

	for fn in common_sources:
		##warnings.warn(f'FIXME: build-time inclusion of PQClean {fn} into {lib_name}')
		# https://stackoverflow.com/questions/77689317/dynamic-linking-in-python-cffi
		# https://github.com/python-cffi/cffi/issues/43
		# https://github.com/JamesTheAwesomeDude/pypqc/issues/1
		p = (common_dir / fn)
		sources.append(p)

	# 4. included_ffis, extra_compile_args, libraries, include_dirs #

	included_ffis = []

	extra_compile_args = []
	if platform.system() == 'Windows':
		# https://foss.heptapod.net/pypy/cffi/-/issues/516
		# https://www.reddit.com/r/learnpython/comments/175js2u/def_extern_says_im_not_using_it_in_api_mode/
		# https://learn.microsoft.com/en-us/cpp/build/reference/tc-tp-tc-tp-specify-source-file-type?view=msvc-170
		extra_compile_args.append('/TC')

	libraries = []
	if platform.system() == 'Windows':
		# https://stackoverflow.com/questions/69900013/link-error-cannot-build-python-c-extension-in-windows
		# https://learn.microsoft.com/en-us/windows/win32/seccrypto/required-libraries
		libraries.append('Advapi32')

	include_dirs = [(build_root), (common_dir)]

	# 5. create, return #

	ffibuilder = FFI()
	map_immed(ffibuilder.include, included_ffis)
	map_immed(ffibuilder.cdef, cdefs)
	ffibuilder.set_source(
		module_name,
		'\n'.join(c_header_sources),
		sources=[p.as_posix() for p in sources],
		include_dirs=[p.as_posix() for p in include_dirs],
		extra_objects=extra_objects,
		extra_compile_args=extra_compile_args,
		libraries=libraries,
	)
	return ffibuilder
