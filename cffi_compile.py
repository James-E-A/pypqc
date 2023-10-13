from cffi import FFI
ffibuilder = FFI()

from hashlib import shake_256 as hashlib_shake_256
from os import urandom


ffibuilder.set_source("_libmceliece6960119f", """
#include "api.h"
""",
	library_dirs=["Lib/PQClean/crypto_kem/mceliece6960119f/clean"],
	include_dirs=["Lib/PQClean/crypto_kem/mceliece6960119f/clean"],
	libraries=["libmceliece6960119f_clean"]
)


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
}

int PQCLEAN_MCELIECE6960119F_CLEAN_crypto_kem_enc(
	uint8_t *c,
	uint8_t *key,
	const uint8_t *pk
);

int PQCLEAN_MCELIECE6960119F_CLEAN_crypto_kem_dec(
	uint8_t *key,
	const uint8_t *c,
	const uint8_t *sk
);

int PQCLEAN_MCELIECE6960119F_CLEAN_crypto_kem_keypair
(
	uint8_t *pk,
	uint8_t *sk
);
""")


if __name__ == "__main__":
	import os
	assert (os.name != 'nt') or ('x64' == os.environ['VSCMD_ARG_TGT_ARCH'] == os.environ['VSCMD_ARG_HOST_ARCH']), "https://visualstudio.microsoft.com/visual-cpp-build-tools/\nCall this script from within \"Developer Command Prompt for VS 2022\""
	
	ffibuilder.compile(verbose=True)

	from _libmceliece6960119f import lib as libmceliece6960119f, ffi as ffi


	@ffi.def_extern(name="shake256")  # Crashes on this line
	def _impl_shake256(output, outlen, input_, inlen):
		input_buf = ffi.buffer(input_, inlen)
		h = hashlib_shake_256(input_buf)
		tmp = h.digest(outlen)
		ffi.memmove(output, tmp, len(tmp))


	@ffi.def_extern(name="PQCLEAN_randombytes")
	def _impl_randombytes(output, n):
		tmp = urandom(n)
		ffi.memmove(output, tmp, len(tmp))
		return n

	...
