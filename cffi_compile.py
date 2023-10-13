from cffi import FFI

from distutils.sysconfig import parse_makefile
import hashlib
import os
from pathlib import Path, PurePosixPath
import platform
import re


_IS_WINDOWS = (platform.uname().system == 'Windows')
_IS_x86_64 = (platform.uname().machine == 'AMD64')
_IN_64BIT_VSCMD = ('x64' == os.environ.get('VSCMD_ARG_TGT_ARCH') == os.environ.get('VSCMD_ARG_HOST_ARCH'))
if (_IS_WINDOWS) and (_IS_x86_64) and (not _IN_64BIT_VSCMD):
	# Impossible-to-debug problems arise if this is neglected
	raise AssertionError("Call this script from *within* \"Developer Command Prompt for VS 2022\"\nhttps://visualstudio.microsoft.com/visual-cpp-build-tools/")


def main(src='Lib/PQClean'):
	COMMON_INCLUDE = Path(src) / 'common'
	for kem_alg in (Path(src) / 'crypto_kem').iterdir():
		if 'hqc-rmrs' in kem_alg.name:
			continue  # TODO
		if 'kyber' in kem_alg.name:
			continue  # TODO

		module_name = '_' + kem_alg.name
		BUILD_ROOT = kem_alg / "clean"
		ffibuilder = FFI()

		source_files = parse_makefile(BUILD_ROOT / 'Makefile')['SOURCES'].split()
		sources = [PurePosixPath(BUILD_ROOT / f) for f in source_files]
		sources = [p for p in sources if not p.name.startswith('aes')]  # I HAVE NO IDEA WHY THIS LINE IS REQUIRED
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

		ffibuilder.cdef("""
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
		}""")

		ffibuilder.compile(verbose=True)


if __name__ == "__main__":
	main()
