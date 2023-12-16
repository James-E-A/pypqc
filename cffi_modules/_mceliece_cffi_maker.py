from cffi import FFI

from distutils.sysconfig import parse_makefile
from pathlib import Path
import platform
import re
from textwrap import dedent

from pqc._util import partition_list, map_immed

_NAMESPACE_RE = re.compile(r'(?ms)^#define\s+(CRYPTO_NAMESPACE)\s*\(\s*(\w+)\s*\)\s+(\w+)\s+##\s*\2\s*$')

def make_ffi(build_root):
	build_root = Path(build_root)
	lib_name = build_root.parent.name
	variant = build_root.name
	assert lib_name.startswith('mceliece')
	module_name = f'pqc._lib.{lib_name}_{variant}'
	namespace = _NAMESPACE_RE.search((build_root / 'namespace.h').read_text()).group(3)

	ffibuilder = FFI()
	extra_compile_args = []
	csources = []
	cdefs = []

	# Public Interface

	source_names = parse_makefile(build_root / 'Makefile')['SOURCES'].split()
	source_names.remove('aes256ctr.c')  # Test infrastructure only
	sources = [(build_root / fn) for fn in source_names]

	sources, extra_objects = partition_list(lambda p: p.suffix == '.c', sources)

	include = [(build_root / '../../../common'), (build_root / 'api.h'), (build_root / 'params.h')]
	include_h = [p.name for p in include if not p.is_dir()]
	include_dirs = list({(p.parent if not p.is_dir() else p) for p in include})

	csources.append('\n'.join(f'#include "{h}"' for h in include_h))

	cdefs.append(dedent(f"""\
		static const char {namespace}CRYPTO_ALGNAME[...];
		int {namespace}pk_gen(unsigned char *pk, unsigned char *sk, const uint32_t *perm, int16_t *pi, uint64_t *pivots);
		void {namespace}encrypt(unsigned char *s, const unsigned char *pk, unsigned char *e);
		int {namespace}decrypt(unsigned char *e, const unsigned char *sk, const unsigned char *c);
		int {namespace}crypto_kem_keypair(unsigned char *pk, unsigned char *sk);
		int {namespace}crypto_kem_enc(unsigned char *c, unsigned char *key, const unsigned char *pk);
		int {namespace}crypto_kem_dec(unsigned char *key, const unsigned char *c, const unsigned char *sk);
	"""))

	# Platform-specific

	if platform.system() == 'Windows':
		# https://foss.heptapod.net/pypy/cffi/-/issues/516
		# https://www.reddit.com/r/learnpython/comments/175js2u/def_extern_says_im_not_using_it_in_api_mode/
		# https://learn.microsoft.com/en-us/cpp/build/reference/tc-tp-tc-tp-specify-source-file-type?view=msvc-170
		extra_compile_args.append('/TC')

	# Site Interface

	cdefs.append('static const char _NAMESPACE[...];',)
	csources.append(f'static const char _NAMESPACE[] = "{namespace}";',)

	cdefs.append(dedent(f"""\
		typedef uint8_t {namespace}crypto_secretkey[...];
		typedef uint8_t {namespace}crypto_publickey[...];
		typedef uint8_t {namespace}crypto_kem_plaintext[...];
		typedef uint8_t {namespace}crypto_kem_ciphertext[...];
		const int GFBITS;
		const int SYS_N;
		const int SYS_T;
	"""))
	csources.append(dedent(f"""\
		typedef uint8_t {namespace}crypto_secretkey[{namespace}CRYPTO_SECRETKEYBYTES];
		typedef uint8_t {namespace}crypto_publickey[{namespace}CRYPTO_PUBLICKEYBYTES];
		typedef uint8_t {namespace}crypto_kem_plaintext[{namespace}CRYPTO_BYTES];
		typedef uint8_t {namespace}crypto_kem_ciphertext[{namespace}CRYPTO_CIPHERTEXTBYTES];
	"""))


	# Injected Dependencies

	cdefs.append(dedent("""\
		extern "Python+C" {
			void shake256(
				uint8_t *output,
				size_t outlen,
				const uint8_t *input,
				size_t inlen
			);

			int PQCLEAN_randombytes(
				uint8_t *output,
				size_t n
			);

			void sha512(
				uint8_t *out,
				const uint8_t *in,
				size_t inlen
			);
		}
	"""))


	ffibuilder.set_source(
		module_name,
		'\n'.join(csources),
		sources=[p.as_posix() for p in sources],
		include_dirs=[p.as_posix() for p in include_dirs],
		extra_objects=extra_objects,
		extra_compile_args=extra_compile_args,
	)
	map_immed(ffibuilder.cdef, cdefs)
	return ffibuilder
