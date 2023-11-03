# Do NOT import these functions into general-purpose Python code!
# They are CFFI-specific functions!

import hashlib
import os
import functools


def shake256(output, outlen, input_, inlen, *, ffi):
	result = hashlib.shake_256(ffi.buffer(input_, inlen)).digest(outlen)
	assert len(result) <= outlen
	ffi.memmove(output, result, len(result))


def PQCLEAN_randombytes(output, n, *, ffi):
	result = os.urandom(n)
	assert len(result) <= n
	ffi.memmove(output, result, len(result))
	return len(result)
