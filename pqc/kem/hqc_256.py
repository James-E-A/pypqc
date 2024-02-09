from .._lib.libhqc_256_clean import ffi, lib

import os

if os.environ.get('LICENSED_HQC', '0') == '0':
	# fmt: off
	from .._util import patent_notice
	patent_notice(['FR2956541B1/US9094189B2/EP2537284B1'],
	              'the HQC cryptosystem', 3,
	              ['https://csrc.nist.gov/csrc/media/Projects/post-quantum-cryptography/documents/round-4/final-ip-statements/HQC-Statements-Round4.pdf']
	)
	# fmt: on

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
	_pk = ffi.new(_T_PUBLICKEY)
	_sk = ffi.new(_T_SECRETKEY)

	errno = _crypto_kem_keypair(_pk, _sk)

	if errno == 0:
		return bytes(_pk), bytes(_sk)
	raise RuntimeError(f'{_crypto_kem_keypair.__name__} returned error code {errno}')


def encap(pk):
	_ct = ffi.new(_T_KEM_CIPHERTEXT)
	_ss = ffi.new(_T_KEM_PLAINTEXT)
	_pk = ffi.cast(_T_PUBLICKEY, ffi.from_buffer(pk))

	errno = _crypto_kem_enc(_ct, _ss, _pk)

	if errno == 0:
		return bytes(_ss), bytes(_ct)
	raise RuntimeError(f'{_crypto_kem_enc.__name__} returned error code {errno}')


def decap(ciphertext, sk):
	_ss = ffi.new(_T_KEM_PLAINTEXT)
	_ct = ffi.cast(_T_KEM_CIPHERTEXT, ffi.from_buffer(ciphertext))
	_sk = ffi.cast(_T_SECRETKEY, ffi.from_buffer(sk))

	errno = _crypto_kem_dec(_ss, _ct, _sk)

	if errno == 0:
		return bytes(_ss)
	raise RuntimeError(f'{_crypto_kem_dec.__name__} returned error code {errno}')
