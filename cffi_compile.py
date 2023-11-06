from cffi import FFI

from distutils.sysconfig import parse_makefile
import hashlib
import os
from pathlib import Path, PurePosixPath
import platform
import re


_IS_WINDOWS = (platform.system() == 'Windows')
_IS_x86_64 = (platform.machine() == 'AMD64')
_IS_x86 = (platform.machine() in {'i386', 'i686', 'x86'})
_IN_x86_64_VSCMD = ('x64' == os.environ.get('VSCMD_ARG_TGT_ARCH'))
_IN_x86_VSCMD = ('x32' == os.environ.get('VSCMD_ARG_TGT_ARCH'))
if (_IS_WINDOWS) and (((_IS_x86_64) and (not _IN_x86_64_VSCMD)) or ((_IS_x86) and (not _IN_x86_VSCMD))):
	# Painful-to-debug problems for the caller arise if this is neglected
	raise AssertionError("Call this script from *within* \"Developer Command Prompt for VS 2022\"\nhttps://visualstudio.microsoft.com/visual-cpp-build-tools/")


_CDEF_EXTRA = """
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
}"""

_CDEF_RE = re.compile(r'(?ms)^\s*(?:#define\s+\w+ \d+|\w[\w ]*\s(\w+)\s*\(.*?\);)$')
_NAMESPACE_RE = re.compile(r'(?ms)^#define\s+(CRYPTO_NAMESPACE)\s*\(\s*(\w+)\s*\)\s+(\w+)\s+##\s*\2\s*$')


def main(src='Lib/PQClean'):
	src = Path(src)
	COMMON_INCLUDE = src / 'common'
	for kem_alg in (src / 'crypto_kem').iterdir():
		alg_name = kem_alg.name
		if alg_name.startswith('hqc-rmrs'):
			continue  # TODO
		if alg_name.startswith('kyber'):
			continue  # TODO needs miscellaneous shake256_* suite functions

		for BUILD_ROOT in (p for p in kem_alg.iterdir() if p.is_dir()):
			variant = BUILD_ROOT.name
			if variant == 'clean':
				variant = None

			if variant == 'avx2':
				continue  # TODO this raises "too few actual parameters for intrinsic function"

			if variant == 'aarch64':
				continue  # TODO figure out cross-compiling

			if alg_name.startswith('mceliece'):
				if alg_name.endswith('f'):
					alg_name = alg_name[:-1]
				else:
					if variant is None:
						variant = 'ref'
					else:
						variant = f'{variant}_ref'

			if variant is not None:
				module_name = f'pqc.crypto_kem._{alg_name}_{variant}'
			else:
				module_name = f'pqc.crypto_kem._{alg_name}'

			extra_compile_args = []
			if _IS_WINDOWS:
				# https://www.reddit.com/r/learnpython/comments/175js2u/def_extern_says_im_not_using_it_in_api_mode/k4qit36/
				extra_compile_args.append('/TC')

			object_names = parse_makefile(BUILD_ROOT / 'Makefile')['OBJECTS'].split()
			object_names = [fn for fn in object_names if not fn.startswith('aes')]  # Not sure why this is necessary

			objects = [(BUILD_ROOT / fn) for fn in object_names]

			sources = [p.with_suffix('.c') for p in objects]

			include = [COMMON_INCLUDE, (BUILD_ROOT / 'api.h'), (BUILD_ROOT / 'params.h')]
			include_dirs=list({PurePosixPath(p.parent if not p.is_dir() else p) for p in include})
			c_header_source = "\n".join(f"#include <{p.name}>" for p in include if not p.is_dir())

			ffibuilder = FFI()

			ffibuilder.set_source(module_name, c_header_source,
				include_dirs=include_dirs,
				sources=sources,
				extra_compile_args=extra_compile_args
			)

			# SYS_N
			# SYS_T
			c_header_source = (BUILD_ROOT / 'params.h').read_text()
			c_header_source = "\n".join(m[0] for m in _CDEF_RE.finditer(c_header_source))
			ffibuilder.cdef(c_header_source)

			pfxsentinel, _, pfx = _NAMESPACE_RE.search((BUILD_ROOT / 'namespace.h').read_text()).groups()

			# crypto_kem_enc
			# crypto_kem_dec
			# crypto_kem_keypair
			c_header_source = (BUILD_ROOT / 'crypto_kem.h').read_text()
			func_names = [m[1] for m in re.finditer(fr'(?ms)^#define\s+(\w+)\s+{re.escape(pfxsentinel)}\s*\(\s*\1\s*\)\s*$', c_header_source)]
			c_header_source = (BUILD_ROOT / 'operations.h').read_text()
			c_header_source = "\n".join(m[0] for m in _CDEF_RE.finditer(c_header_source))
			c_header_source = re.sub(fr'(?:{"|".join(map(re.escape, func_names))})', lambda m: pfx + m[0], c_header_source)
			ffibuilder.cdef(c_header_source)

			# encrypt
			# decrypt
			# pk_gen
			for fn in ['encrypt', 'decrypt', 'pk_gen']:
				c_header_source = (BUILD_ROOT / f"{fn}.h").read_text()
				func_name = re.search(fr'(?ms)^#define\s+(\w+)\s+{re.escape(pfxsentinel)}\s*\(\s*\1\s*\)\s*$', c_header_source)[1]
				c_header_source = "\n".join(m[0] for m in _CDEF_RE.finditer(c_header_source))
				c_header_source = re.sub(re.escape(func_name), lambda m: pfx + m[0], c_header_source)
				ffibuilder.cdef(c_header_source)

			ffibuilder.cdef(_CDEF_EXTRA)

			ffibuilder.compile(verbose=True, parallel=True)  # https://github.com/python-cffi/cffi/pull/30.diff

	for kem_alg in (src / 'crypto_sign').iterdir():
		continue  # TODO


if __name__ == "__main__":
	main()
