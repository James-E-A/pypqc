from hashlib import shake_256
from os import urandom as randombytes


def _impl_shake256(output, outlen, input_, inlen, *, ffi):
	result = shake_256(ffi.buffer(input_, inlen)).digest(outlen)
	assert len(result) <= outlen  # TODO check if FFI needs this or is already memory-safe
	ffi.memmove(output, result, len(result))


def _impl_randombytes(output, n, *, ffi):
	result = randombytes(n)
	assert len(result) <= n  # TODO check if FFI needs this or is already memory-safe
	ffi.memmove(output, result, len(result))
	return len(result)
