from cffi import FFI
import hashlib
import os
ffi = FFI()

import _mceliece6960119f

def _impl_shake256(output, outlen, input_, inlen, *, ffi=ffi):
	result = hashlib.shake_256(ffi.buffer(input_, inlen)).digest(outlen)
	assert len(result) <= outlen
	ffi.memmove(output, result, len(result))


def _impl_randombytes(output, n, *, ffi=ffi):
	result = os.urandom(n)
	assert len(result) <= n
	ffi.memmove(output, result, len(result))
	return len(result)


_mceliece6960119f.ffi.def_extern(name="shake256")(_impl_shake256)
_mceliece6960119f.ffi.def_extern(name="PQCLEAN_randombytes")(_impl_randombytes)


def mceliece6960119f_keypair():
	pk = ffi.from_buffer(bytearray(_mceliece6960119f.lib.PQCLEAN_MCELIECE6960119F_CLEAN_CRYPTO_PUBLICKEYBYTES))
	sk = ffi.from_buffer(bytearray(_mceliece6960119f.lib.PQCLEAN_MCELIECE6960119F_CLEAN_CRYPTO_SECRETKEYBYTES))

	_mceliece6960119f.lib.PQCLEAN_MCELIECE6960119F_CLEAN_crypto_kem_keypair(pk, sk)

	return ffi.buffer(pk)[:], ffi.buffer(sk)[:]


def mceliece6960119f_enc(pk, data):
        ...


def mceliece6960119f_dec(sk, data):
        ...
