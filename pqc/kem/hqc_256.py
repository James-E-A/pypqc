from .._lib.libhqc_256_clean import ffi, lib

import os
if os.environ.get('LICENSED_HQC', '0') == '0':
	from .._util import patent_notice
	patent_notice(['FR2956541B1/US9094189B2/EP2537284B1'],
	              'the HQC cryptosystem', 3,
	              ['https://csrc.nist.gov/csrc/media/Projects/post-quantum-cryptography/documents/round-4/final-ip-statements/HQC-Statements-Round4.pdf']
	)

__all__ = ['keypair', 'encap', 'decap']

_LIB_NAMESPACE = ffi.string(lib._NAMESPACE).decode('ascii')
_T_PUBLICKEY = f'{_LIB_NAMESPACE}crypto_publickey'
_T_SECRETKEY = f'{_LIB_NAMESPACE}crypto_secretkey'
_T_KEM_PLAINTEXT = f'{_LIB_NAMESPACE}crypto_kem_plaintext'
_T_KEM_CIPHERTEXT = f'{_LIB_NAMESPACE}crypto_kem_ciphertext'

_crypto_kem_keypair = getattr(lib, f'{_LIB_NAMESPACE}crypto_kem_keypair')
_crypto_kem_enc = getattr(lib, f'{_LIB_NAMESPACE}crypto_kem_enc')
_crypto_kem_dec = getattr(lib, f'{_LIB_NAMESPACE}crypto_kem_dec')


def keypair():
	pk = ffi.new(_T_PUBLICKEY)
	sk = ffi.new(_T_SECRETKEY)

	errno = _crypto_kem_keypair(ffi.cast('char*', pk), ffi.cast('char*', sk))

	if errno:
		raise RuntimeError(f"{_crypto_kem_keypair.__name__} returned error code {errno}")
	return bytes(pk), bytes(sk)


def encap(pk):
	ciphertext = ffi.new(_T_KEM_CIPHERTEXT)
	key = ffi.new(_T_KEM_PLAINTEXT)
	pk = ffi.cast(_T_PUBLICKEY, ffi.from_buffer(pk))

	errno = _crypto_kem_enc(ffi.cast('char*', ciphertext), ffi.cast('char*', key), ffi.cast('char*', pk))

	if errno:
		raise RuntimeError(f"{_crypto_kem_enc.__name__} returned error code {errno}")

	return bytes(key), bytes(ciphertext)


def decap(ciphertext, sk):
	key = ffi.new(_T_KEM_PLAINTEXT)
	ciphertext = ffi.cast(_T_KEM_CIPHERTEXT, ffi.from_buffer(ciphertext))
	sk = ffi.cast(_T_SECRETKEY, ffi.from_buffer(sk))

	errno = _crypto_kem_dec(ffi.cast('char*', key), ffi.cast('char*', ciphertext), ffi.cast('char*', sk))

	if errno:
		raise RuntimeError(f"{_crypto_kem_dec.__name__} returned error code {errno}")

	return bytes(key)

