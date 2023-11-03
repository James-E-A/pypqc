from .crypto_kem import _mceliece6960119

import hashlib
import os


def demo_keypair():
	"""MCELIECE6960119F - Returns *publickey*, *secretkey*.
	"""

	pk = bytearray(_mceliece6960119.lib.PQCLEAN_MCELIECE6960119F_CLEAN_CRYPTO_PUBLICKEYBYTES)
	sk = bytearray(_mceliece6960119.lib.PQCLEAN_MCELIECE6960119F_CLEAN_CRYPTO_SECRETKEYBYTES)

	_mceliece6960119.lib.PQCLEAN_MCELIECE6960119F_CLEAN_crypto_kem_keypair(
	    _mceliece6960119.ffi.from_buffer(pk),
	    _mceliece6960119.ffi.from_buffer(sk))

	return bytes(pk), bytes(sk)


def demo_kem_enc(pk):
	"""MCELIECE6960119F - Accepts *publickey*; returns *shared_secret*, *kem_ciphertext*.
	"""

	ciphertext = bytearray(_mceliece6960119.lib.PQCLEAN_MCELIECE6960119F_CLEAN_CRYPTO_CIPHERTEXTBYTES)
	shared_key = bytearray(_mceliece6960119.lib.PQCLEAN_MCELIECE6960119F_CLEAN_CRYPTO_BYTES)

	_mceliece6960119.lib.PQCLEAN_MCELIECE6960119F_CLEAN_crypto_kem_enc(
	    _mceliece6960119.ffi.from_buffer(ciphertext),
	    _mceliece6960119.ffi.from_buffer(shared_key),
	    pk)

	return bytes(shared_key), bytes(ciphertext)


def demo_kem_dec(sk, ciphertext):
	"""MCELIECE6960119F - Accepts *privatekey*, *kem_ciphertext*; returns *shared_secret*.
	"""

	shared_key = bytearray(_mceliece6960119.lib.PQCLEAN_MCELIECE6960119F_CLEAN_CRYPTO_BYTES)

	_mceliece6960119.lib.PQCLEAN_MCELIECE6960119F_CLEAN_crypto_kem_dec(
	    _mceliece6960119.ffi.from_buffer(shared_key),
	    ciphertext,
	    sk)

	return bytes(shared_key)

if __name__ == '__main__':
	public_key, secret_key = demo_keypair()
	test_key, test_ciphertext = demo_kem_enc(public_key)
	test_decrypted = demo_kem_dec(secret_key, test_ciphertext)

	if test_key != test_decrypted:
		raise AssertionError("fail :(")
	print("OK")
