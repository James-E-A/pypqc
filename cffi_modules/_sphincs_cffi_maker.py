from cffi import FFI

from distutils.sysconfig import parse_makefile
from pathlib import Path
import platform
import re
from textwrap import dedent

from pqc._util import partition_list, map_immed, fix_compile_args, fix_libraries

_NAMESPACE_RE = re.compile(r'(?ms)^#define\s+(SPX_NAMESPACE)\s*\(\s*(\w+)\s*\)\s+(\w+)##\2\s*$')

def make_ffi(build_root, *, parent_module='pqc._lib'):
	build_root = Path(build_root)
	makefile_parsed = parse_makefile(build_root / 'Makefile')
	common_dir = build_root / '..' / '..' / '..' / 'common'

	_lib_name = Path(makefile_parsed['LIB']).stem
	lib_name = _lib_name.replace('-', '_')
	assert lib_name.startswith('libsphincs')
	module_name = f'{parent_module}.{lib_name}'
	namespace = _NAMESPACE_RE.search((build_root / 'params.h').read_text()).group(3)

	included_ffis = []
	extra_compile_args = []
	libraries = []
	c_header_sources = []
	cdefs = []


	_object_names = makefile_parsed['OBJECTS'].split()
	sources = [(build_root / fn).with_suffix('.c') for fn in _object_names]

	include_dirs = [(build_root), (common_dir)]

	cdefs.append(dedent(f"""\
	// Public KEM interface
	static const char {namespace}CRYPTO_ALGNAME[...];
	int {namespace}crypto_sign_keypair(uint8_t *pk, uint8_t *sk);
	int {namespace}crypto_sign_signature(uint8_t *sig, size_t *siglen, const uint8_t *m, size_t mlen, const uint8_t *sk);
	int {namespace}crypto_sign_verify(const uint8_t *sig, size_t siglen, const uint8_t *m, size_t mlen, const uint8_t *pk);
	int {namespace}crypto_sign(uint8_t *sm, size_t *smlen, const uint8_t *m, size_t mlen, const uint8_t *sk);
	int {namespace}crypto_sign_open(uint8_t *m, size_t *mlen, const uint8_t *sm, size_t smlen, const uint8_t *pk);
	"""))

	c_header_sources.append(dedent("""\
	// Public signature interface
	#include "api.h"
	"""))

	cdefs.append(dedent(f"""\
	// Exposed internal interface
	// ... TODO
	"""))

	c_header_sources.append(dedent("""\
	// Exposed internal interface
	// ... TODO
	"""))

	cdefs.append(dedent(f"""\
	// Site interface
	static const char _NAMESPACE[...];
	typedef uint8_t {namespace}crypto_secretkey[...];
	typedef uint8_t {namespace}crypto_publickey[...];
	typedef uint8_t {namespace}crypto_signature[...];
	"""))

	c_header_sources.append(dedent(f"""\
	// Site interface
	static const char _NAMESPACE[] = "{namespace}";
	typedef uint8_t {namespace}crypto_secretkey[{namespace}CRYPTO_SECRETKEYBYTES];
	typedef uint8_t {namespace}crypto_publickey[{namespace}CRYPTO_PUBLICKEYBYTES];
	typedef uint8_t {namespace}crypto_signature[{namespace}CRYPTO_BYTES];
	"""))


	_hash_name = re.match(r'libsphincs-(\w+)', _lib_name).group(1)
	_hash_src = {'sha2': 'sha2.c', 'shake': 'fips202.c'}[_hash_name]
	sources.append((common_dir / _hash_src))
	sources.append((common_dir / 'randombytes.c'))


	ffibuilder = FFI()
	map_immed(ffibuilder.include, included_ffis)
	map_immed(ffibuilder.cdef, cdefs)
	fix_compile_args(extra_compile_args)
	fix_libraries(libraries)
	ffibuilder.set_source(
		module_name,
		'\n'.join(c_header_sources),
		sources=[p.as_posix() for p in sources],
		include_dirs=[p.as_posix() for p in include_dirs],
		extra_compile_args=extra_compile_args,
		libraries=libraries,
	)
	return ffibuilder
