# Do NOT import these functions into general-purpose Python code!
# They are C API dependencies for PQClean speciically!

# Currently, monkey-patching this module will *NOT* work as expected;
# graceful monkey-patching support is TODO.

from hashlib import shake_256 as _shake_256
from os import urandom as _urandom


def shake256(output, outlen, input_, inlen, *, ffi):
	result = _shake_256(ffi.buffer(input_, inlen)).digest(outlen)
	assert len(result) <= outlen
	ffi.memmove(output, result, len(result))


def PQCLEAN_randombytes(output, n, *, ffi):
	result = _urandom(n)
	assert len(result) <= n
	ffi.memmove(output, result, len(result))
	return len(result)
