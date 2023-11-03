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


def main(src='Lib/PQClean'):
	COMMON_INCLUDE = Path(src) / 'common'
	for kem_alg in (Path(src) / 'crypto_kem').iterdir():
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

			ffibuilder = FFI()

			objects = [PurePosixPath(BUILD_ROOT / fname) for fname in parse_makefile(BUILD_ROOT / 'Makefile')['OBJECTS'].split()]
			sources = [p.with_suffix('.c') for p in objects if not p.name.startswith('aes')]
			include_dirs = [PurePosixPath(BUILD_ROOT), PurePosixPath(COMMON_INCLUDE)]
			ffibuilder.set_source(module_name, """
				#include "api.h"
			""",
				include_dirs=include_dirs,
				sources=sources,
				extra_compile_args=(["/TC"] if os.name == 'nt' else None),  # https://www.reddit.com/r/learnpython/comments/175js2u/def_extern_says_im_not_using_it_in_api_mode/k4qit36/
			)

			api_source = BUILD_ROOT / 'api.h'
			for c_src in re.findall(r'(?ms)^(#define \w+ \d+|[\w ]+\s*\(.*?\);)$', api_source.read_text()):
				ffibuilder.cdef(c_src)

			ffibuilder.cdef(_CDEF_EXTRA)

			ffibuilder.compile(verbose=True, parallel=True)


if __name__ == "__main__":
	main()
