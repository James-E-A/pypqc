import _mceliece6960119f

from cffi import FFI
import hashlib
import os


@_mceliece6960119f.ffi.def_extern(name="shake256")
def _impl_shake256(output, outlen, input_, inlen, *, ffi=_mceliece6960119f.ffi):
	result = hashlib.shake_256(ffi.buffer(input_, inlen)).digest(outlen)
	assert len(result) <= outlen
	ffi.memmove(output, result, len(result))


@_mceliece6960119f.ffi.def_extern(name="PQCLEAN_randombytes")
def _impl_randombytes(output, n, *, ffi=_mceliece6960119f.ffi):
	result = os.urandom(n)
	assert len(result) <= n
	ffi.memmove(output, result, len(result))
	return len(result)


def demo_keypair():
	"""MCELIECE6960119F - Returns *publickey*, *secretkey*.
	"""
	pk = bytearray(_mceliece6960119f.lib.PQCLEAN_MCELIECE6960119F_CLEAN_CRYPTO_PUBLICKEYBYTES)
	_pk = _mceliece6960119f.ffi.from_buffer(pk)

	sk = bytearray(_mceliece6960119f.lib.PQCLEAN_MCELIECE6960119F_CLEAN_CRYPTO_SECRETKEYBYTES)
	_sk = _mceliece6960119f.ffi.from_buffer(sk)

	_mceliece6960119f.lib.PQCLEAN_MCELIECE6960119F_CLEAN_crypto_kem_keypair(_pk, _sk)

	return bytes(pk), bytes(sk)


def demo_kem_enc(pk):
	"""MCELIECE6960119F - Accepts *publickey*; returns *shared_secret*, *kem_ciphertext*.
	"""

	ciphertext = bytearray(_mceliece6960119f.lib.PQCLEAN_MCELIECE6960119F_CLEAN_CRYPTO_CIPHERTEXTBYTES)
	_c = _mceliece6960119f.ffi.from_buffer(ciphertext)

	shared_key = bytearray(_mceliece6960119f.lib.PQCLEAN_MCELIECE6960119F_CLEAN_CRYPTO_BYTES)
	_key = _mceliece6960119f.ffi.from_buffer(shared_key)

	_pk = _mceliece6960119f.ffi.from_buffer(pk)
	assert len(_pk) == _mceliece6960119f.lib.PQCLEAN_MCELIECE6960119F_CLEAN_CRYPTO_PUBLICKEYBYTES

	_mceliece6960119f.lib.PQCLEAN_MCELIECE6960119F_CLEAN_crypto_kem_enc(_c, _key, _pk)

	return bytes(shared_key), bytes(ciphertext)


def demo_kem_dec(sk, ciphertext):
	"""MCELIECE6960119F - Accepts *privatekey*, *kem_ciphertext*; returns *shared_secret*.
	"""

	shared_key = bytearray(_mceliece6960119f.lib.PQCLEAN_MCELIECE6960119F_CLEAN_CRYPTO_BYTES)
	_key = _mceliece6960119f.ffi.from_buffer(shared_key)

	_c = _mceliece6960119f.ffi.from_buffer(ciphertext)
	assert len(_c) == _mceliece6960119f.lib.PQCLEAN_MCELIECE6960119F_CLEAN_CRYPTO_CIPHERTEXTBYTES

	_sk = _mceliece6960119f.ffi.from_buffer(sk)
	assert len(_sk) == _mceliece6960119f.lib.PQCLEAN_MCELIECE6960119F_CLEAN_CRYPTO_SECRETKEYBYTES

	_mceliece6960119f.lib.PQCLEAN_MCELIECE6960119F_CLEAN_crypto_kem_dec(_key, _c, _sk)

	return bytes(shared_key)


if __name__ == '__main__':
	public_key, secret_key = demo_keypair()
	#print(f"Public key:\n{public_key[:7].hex()}")
	#print(f"Private key:\n{secret_key[:7].hex()}")

	test_key, test_ciphertext = demo_kem_enc(public_key)
	#print(f"Shared secret:\n{test_message[:7].hex()}")
	#print(f"Ciphertext:\n{test_ciphertext[:7].hex()}")

	test_decrypted = demo_kem_dec(secret_key, test_ciphertext)
	#print(f"Decrypted:\n{test_decrypted[:7].hex()}")

	#print("INTEGRITY CHECK:")
	#print(f"Public key:\n{public_key[:7].hex()}")
	#print(f"Private key:\n{secret_key[:7].hex()}")
	#print(f"Shared secret:\n{test_message[:7].hex()}")

	assert test_key == test_decrypted, "fail :("
