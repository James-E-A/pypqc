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


def demo_keypair():
	"""MCELIECE6960119F - Returns *publickey*, *secretkey*.
	"""
	pk = bytearray(_mceliece6960119f.lib.PQCLEAN_MCELIECE6960119F_CLEAN_CRYPTO_PUBLICKEYBYTES)
	sk = bytearray(_mceliece6960119f.lib.PQCLEAN_MCELIECE6960119F_CLEAN_CRYPTO_SECRETKEYBYTES)

	_mceliece6960119f.lib.PQCLEAN_MCELIECE6960119F_CLEAN_crypto_kem_keypair(_mceliece6960119f.ffi.from_buffer(pk), _mceliece6960119f.ffi.from_buffer(sk))

	return bytes(pk), bytes(sk)


def demo_kem_enc(pk, data):
	"""MCELIECE6960119F - Accepts *publickey*, *shared_secret*; returns *kem_ciphertext*.
	"""
	assert len(data) == _mceliece6960119f.lib.PQCLEAN_MCELIECE6960119F_CLEAN_CRYPTO_BYTES
	assert len(pk) == _mceliece6960119f.lib.PQCLEAN_MCELIECE6960119F_CLEAN_CRYPTO_PUBLICKEYBYTES
	ciphertext = bytearray(_mceliece6960119f.lib.PQCLEAN_MCELIECE6960119F_CLEAN_CRYPTO_CIPHERTEXTBYTES)

	_mceliece6960119f.lib.PQCLEAN_MCELIECE6960119F_CLEAN_crypto_kem_enc(_mceliece6960119f.ffi.from_buffer(ciphertext), _mceliece6960119f.ffi.from_buffer(data), _mceliece6960119f.ffi.from_buffer(pk))

	return bytes(ciphertext)


def demo_kem_dec(sk, data):
	"""MCELIECE6960119F - Accepts *privatekey*, *kem_ciphertext*; returns *shared_secret*.
	"""
	assert len(data) == _mceliece6960119f.lib.PQCLEAN_MCELIECE6960119F_CLEAN_CRYPTO_CIPHERTEXTBYTES
	assert len(sk) == _mceliece6960119f.lib.PQCLEAN_MCELIECE6960119F_CLEAN_CRYPTO_SECRETKEYBYTES
	plaintext = bytearray(_mceliece6960119f.lib.PQCLEAN_MCELIECE6960119F_CLEAN_CRYPTO_BYTES)

	_mceliece6960119f.lib.PQCLEAN_MCELIECE6960119F_CLEAN_crypto_kem_dec(_mceliece6960119f.ffi.from_buffer(plaintext), _mceliece6960119f.ffi.from_buffer(data), _mceliece6960119f.ffi.from_buffer(sk))

	return bytes(plaintext)
