from cffi import FFI

from collections import deque
from distutils.sysconfig import parse_makefile
import hashlib
import os
from pathlib import Path
import platform
import re
from setuptools import build_meta as _orig_setuptools_backend
from setuptools.build_meta import *
from setuptools import Extension
from textwrap import dedent


_IS_WINDOWS = (platform.system() == 'Windows')
_IS_x86_64 = (platform.machine() == 'AMD64')
_IS_x86 = (platform.machine() in {'i386', 'i686', 'x86'})
_IN_x86_64_VSCMD = ('x64' == os.environ.get('VSCMD_ARG_TGT_ARCH'))
_IN_x86_VSCMD = ('x32' == os.environ.get('VSCMD_ARG_TGT_ARCH'))
if (_IS_WINDOWS) and (((_IS_x86_64) and (not _IN_x86_64_VSCMD)) or ((_IS_x86) and (not _IN_x86_VSCMD))):
	# Painful-to-debug problems for the caller arise if this is neglected
	raise AssertionError("Call this script from *within* \"Developer Command Prompt for VS 2022\"\nhttps://visualstudio.microsoft.com/visual-cpp-build-tools/")


_CDEF_RE = re.compile(r'(?ms)^\s*(#define\s+\w+ \d+|\w[\w ]*\s(\w+)\s*\(.*?\);)$')
_NAMESPACE_RE = re.compile(r'(?ms)^#define\s+(CRYPTO_NAMESPACE)\s*\(\s*(\w+)\s*\)\s+(\w+)\s+##\s*\2\s*$')
_NAMESPACED_RE = re.compile(r'(?ms)^#define\s+(\w+)\s+CRYPTO_NAMESPACE\s*\(\s*\1\s*\)\s*$')


def _main(src='.'):
	pqc_root = Path(src) / 'Lib/PQClean'
	COMMON_INCLUDE = pqc_root / 'common'
	for kem_alg_src in (pqc_root / 'crypto_kem').iterdir():
		alg_name = kem_alg_src.name
		if alg_name.startswith('hqc-rmrs'):
			continue  # TODO
		if alg_name.startswith('kyber'):
			continue  # TODO needs miscellaneous shake256_* suite functions

		for BUILD_ROOT in (p for p in kem_alg_src.iterdir() if p.is_dir()):
			variant = BUILD_ROOT.name
			if variant == 'clean':
				variant = ''

			if variant == 'avx2':
				# TODO
				# mceliece348864\avx2\util.h(110): error C2440: 'type cast': cannot convert from 'vec128' to 'vec128'
				continue

				if not (_IS_x86_64 or _IS_x86):
					continue

			if variant == 'aarch64':
				continue  # TODO figure out cross-compiling

			if alg_name.startswith('mceliece'):
				if alg_name.endswith('f'):
					# "fast" key generation
					alg_name = alg_name[:-1]
				else:
					# "simple" key generation
					# (unclear if this has any
					# use beyond the existence
					# of the source code itself)
					variant = f'{f"{variant}_" if variant else ""}ref'

			module_name = f'pqc.kem._{alg_name}{f"_{variant}" if variant else ""}'

			extra_compile_args = []
			if _IS_WINDOWS:
				# https://foss.heptapod.net/pypy/cffi/-/issues/516
				# https://www.reddit.com/r/learnpython/comments/175js2u/def_extern_says_im_not_using_it_in_api_mode/
				# https://learn.microsoft.com/en-us/cpp/build/reference/tc-tp-tc-tp-specify-source-file-type?view=msvc-170
				extra_compile_args.append('/TC')

			cdefs = []

			namespace = _NAMESPACE_RE.search((BUILD_ROOT / 'namespace.h').read_text()).group(3)

			# PQClean-provided interface
			cdefs.append(dedent(f"""\
				static const char {namespace}CRYPTO_ALGNAME[...];
				int {namespace}pk_gen(unsigned char *pk, unsigned char *sk, const uint32_t *perm, int16_t *pi, uint64_t *pivots);
				void {namespace}encrypt(unsigned char *s, const unsigned char *pk, unsigned char *e);
				int {namespace}decrypt(unsigned char *e, const unsigned char *sk, const unsigned char *c);
				int {namespace}crypto_kem_keypair(unsigned char *pk, unsigned char *sk);
				int {namespace}crypto_kem_enc(unsigned char *c, unsigned char *key, const unsigned char *pk);
				int {namespace}crypto_kem_dec(unsigned char *key, const unsigned char *c, const unsigned char *sk);
			"""))

			# Our internal interface
			cdefs.append(dedent(f"""\
				static const char _NAMESPACE[...];
				typedef uint8_t _{namespace}CRYPTO_SECRETKEY[...];
				typedef uint8_t _{namespace}CRYPTO_PUBLICKEY[...];
				typedef uint8_t _{namespace}CRYPTO_KEM_PLAINTEXT[...];
				typedef uint8_t _{namespace}CRYPTO_KEM_CIPHERTEXT[...];
			"""))
			bonus_csource = dedent(f"""\
				typedef uint8_t _{namespace}CRYPTO_SECRETKEY[{namespace}CRYPTO_SECRETKEYBYTES];
				typedef uint8_t _{namespace}CRYPTO_PUBLICKEY[{namespace}CRYPTO_PUBLICKEYBYTES];
				typedef uint8_t _{namespace}CRYPTO_KEM_PLAINTEXT[{namespace}CRYPTO_BYTES];
				typedef uint8_t _{namespace}CRYPTO_KEM_CIPHERTEXT[{namespace}CRYPTO_CIPHERTEXTBYTES];
			""")

			# Our injected dependencies
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

			# PQClean McEliece-specific
			cdefs.append(dedent(f"""\
				const int GFBITS;
				const int SYS_N;
				const int SYS_T;
			"""))

			# Actual source
			object_names = parse_makefile(BUILD_ROOT / 'Makefile')['OBJECTS'].split()
			object_names.remove('aes256ctr.o')  # Test infrastructure only
			objects = [(BUILD_ROOT / fn) for fn in object_names]
			sources = [str(p.with_suffix('.c')) for p in objects]

			include = [COMMON_INCLUDE, (BUILD_ROOT / 'api.h'), (BUILD_ROOT / 'params.h')]
			if 'avx2' in variant.split('_'):
				include += [(BUILD_ROOT / 'vec128.h'), (BUILD_ROOT / 'vec256.h')]
			include_h = '\n'.join(f'#include "{p.name}"' for p in include if not p.is_dir())
			include_dirs = list({(p.parent if not p.is_dir() else p).as_posix() for p in include})

			csource = (
				include_h +
				dedent(f"""
				// low-priority semantics quibble: escaping
				// https://stackoverflow.com/posts/comments/136533801
				static const char _NAMESPACE[] = "{namespace}";
				""") +
				bonus_csource
			)

			from pprint import pprint; print(pprint(locals()))
			yield module_name, {'csource': csource, 'cdefs': cdefs, 'sources': sources, 'include_dirs': include_dirs, 'extra_compile_args': extra_compile_args}

	#for sign_alg_src in (pqc_root / 'crypto_sign').iterdir():
	#	...  # TODO


def _make_ext_modules():
	# https://stackoverflow.com/a/66479252/1874170
	ext_modules = []
	for module_name, opts in _main():
		opts.pop('csource')
		opts.pop('cdefs')
		p = Path('.', *module_name.split('.')).with_suffix('.c')
		sources = [p.as_posix()]
		sources += opts.pop('sources')
		ext_module = Extension(module_name, sources, **opts)
		ext_modules.append(ext_module)
	return ext_modules


def _mkffi(spec):
	module_name, opts = spec
	ffibuilder = FFI()
	csource = opts.pop('csource')
	cdefs = opts.pop('cdefs')
	ffibuilder.set_source(module_name, csource, **opts)
	deque(map(ffibuilder.cdef, cdefs), 0)
	return ffibuilder


def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
	for ffibuilder in map(_mkffi, _main()):
		ffibuilder.compile(verbose=True)
	return _orig_setuptools_backend.build_wheel(wheel_directory, config_settings=config_settings, metadata_directory=metadata_directory)

