from ._common_cffi_maker import make_pqclean_ffi
from textwrap import dedent

def make_dilithium_ffi(build_root):
	cdefs = []
	c_header_sources = []
	common_sources = ['fips202.c', 'randombytes.c']

	cdefs.append(dedent("""\
	// Public signature interface
	int %(namespace)scrypto_sign_keypair(uint8_t *pk, uint8_t *sk);
	int %(namespace)scrypto_sign_signature(uint8_t *sig, size_t *siglen, const uint8_t *m, size_t mlen, const uint8_t *sk);
	int %(namespace)scrypto_sign_verify(const uint8_t *sig, size_t siglen, const uint8_t *m, size_t mlen, const uint8_t *pk);
	"""))

	c_header_sources.append(dedent("""\
	// Public signature interface
	#include "api.h"
	"""))

	cdefs.append(dedent(f"""\
	// Exposed internal interface
	int %(namespace)scrypto_sign(uint8_t *sm, size_t *smlen, const uint8_t *m, size_t mlen, const uint8_t *sk);
	int %(namespace)scrypto_sign_open(uint8_t *m, size_t *mlen, const uint8_t *sm, size_t smlen, const uint8_t *pk);
	#define CRHBYTES ...
	#define RNDBYTES ...
	#define N ...
	#define Q ...
	#define D ...
	#define ROOT_OF_UNITY ...
	#define K ...
	#define L ...
	#define ETA ...
	#define TAU ...
	#define BETA ...
	#define GAMMA1 ...
	#define GAMMA2 ...
	#define OMEGA ...
	#define CTILDEBYTES ...
	"""))

	c_header_sources.append(dedent("""\
	// Exposed internal interface
	#include "params.h"
	"""))

	cdefs.append(dedent(f"""\
	// Site interface
	static const char _NAMESPACE[...];
	typedef uint8_t %(namespace)scrypto_secretkey[...];
	typedef uint8_t %(namespace)scrypto_publickey[...];
	typedef uint8_t %(namespace)scrypto_signature[...];
	"""))

	c_header_sources.append(dedent(f"""\
	// Site interface
	static const char _NAMESPACE[] = "%(namespace)s";
	typedef uint8_t %(namespace)scrypto_secretkey[%(namespace)sCRYPTO_SECRETKEYBYTES];
	typedef uint8_t %(namespace)scrypto_publickey[%(namespace)sCRYPTO_PUBLICKEYBYTES];
	typedef uint8_t %(namespace)scrypto_signature[%(namespace)sCRYPTO_BYTES];
	"""))

	return make_pqclean_ffi(build_root=build_root, c_header_sources=c_header_sources, cdefs=cdefs, common_sources=common_sources)

def OLD_make_ffi(build_root, *, parent_module='pqc._lib'):
	build_root = Path(build_root)
	makefile_parsed = parse_makefile(build_root / 'Makefile')
	common_dir = build_root / '..' / '..' / '..' / 'common'

	common_sources = [(common_dir / 'fips202.c'), (common_dir / 'randombytes.c')]

	lib_name = Path(makefile_parsed['LIB']).stem
	assert lib_name.startswith('libdilithium')
	module_name = f'{parent_module}.{lib_name}'

	m = _NAMESPACE_RE.search((build_root / 'params.h').read_text())
	if m:
		namespace = m.group(3)
	else:
		warnings.warn(f'falling back to alternate codepath to figure out CRYPTO_NAMESPACE while building {lib_name} from {build_root}')
		m = re.search(r'(?ms)^#define (\w+)CRYPTO_ALGNAME ', (build_root / 'api.h').read_text())
		if m:
			namespace = m.group(1)
		else:
			raise Exception(f"couldn't figure out CRYPTO_NAMESPACE while building {lib_name} from {build_root}")

	included_ffis = []
	extra_compile_args = []
	libraries = []
	c_header_sources = []
	cdefs = []

	if 'SOURCES' in makefile_parsed.keys():
		_source_names = makefile_parsed['SOURCES'].split()
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

	include_dirs = [(build_root), (common_dir)]

	cdefs.append(dedent("""\
	// Public signature interface
	int %(namespace)scrypto_sign_keypair(uint8_t *pk, uint8_t *sk);
	int %(namespace)scrypto_sign_signature(uint8_t *sig, size_t *siglen, const uint8_t *m, size_t mlen, const uint8_t *sk);
	int %(namespace)scrypto_sign_verify(const uint8_t *sig, size_t siglen, const uint8_t *m, size_t mlen, const uint8_t *pk);
	"""))

	c_header_sources.append(dedent("""\
	// Public signature interface
	#include "api.h"
	"""))

	cdefs.append(dedent("""\
	// Exposed internal interface
	int %(namespace)scrypto_sign(uint8_t *sm, size_t *smlen, const uint8_t *m, size_t mlen, const uint8_t *sk);
	int %(namespace)scrypto_sign_open(uint8_t *m, size_t *mlen, const uint8_t *sm, size_t smlen, const uint8_t *pk);
	#define CRHBYTES ...
	#define RNDBYTES ...
	#define N ...
	#define Q ...
	#define D ...
	#define ROOT_OF_UNITY ...
	#define K ...
	#define L ...
	#define ETA ...
	#define TAU ...
	#define BETA ...
	#define GAMMA1 ...
	#define GAMMA2 ...
	#define OMEGA ...
	#define CTILDEBYTES ...
	"""))

	c_header_sources.append(dedent("""\
	// Exposed internal interface
	#include "params.h"
	"""))

	cdefs.append(dedent("""\
	// Site interface
	static const char _NAMESPACE[...];
	typedef uint8_t %(namespace)scrypto_secretkey[...];
	typedef uint8_t %(namespace)scrypto_publickey[...];
	typedef uint8_t %(namespace)scrypto_signature[...];
	"""))

	c_header_sources.append(dedent("""\
	// Site interface
	static const char _NAMESPACE[] = "%(namespace)s";
	typedef uint8_t %(namespace)scrypto_secretkey[%(namespace)sCRYPTO_SECRETKEYBYTES];
	typedef uint8_t %(namespace)scrypto_publickey[%(namespace)sCRYPTO_PUBLICKEYBYTES];
	typedef uint8_t %(namespace)scrypto_signature[%(namespace)sCRYPTO_BYTES];
	"""))

	for p in common_sources:
		# https://stackoverflow.com/questions/77689317/dynamic-linking-in-python-cffi
		# https://github.com/python-cffi/cffi/issues/43
		# https://github.com/JamesTheAwesomeDude/pypqc/issues/1
		warnings.warn(f'FIXME: build-time inclusion of PQClean {p.name} into {lib_name}')
		sources.append(p)

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
		extra_objects=extra_objects,
		extra_compile_args=extra_compile_args,
		libraries=libraries,
	)
	return ffibuilder
