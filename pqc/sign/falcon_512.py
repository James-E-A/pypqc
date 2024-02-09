from .._lib.libfalcon_512_clean import ffi, lib

import os

if os.environ.get('LICENSED_FALCON', '0') == '0':
	# fmt: off
	from .._util import patent_notice
	patent_notice(['US7308097B2'],
	            'the Falcon cryptosystem', 2,
	            ['https://csrc.nist.gov/csrc/media/Projects/post-quantum-cryptography/documents/selected-algos-2022/final-ip-statements/Falcon-Statements-final.pdf#page=20']
	)
	# fmt: on

__all__ = ['keypair', 'sign', 'verify']

_LIB_NAMESPACE = ffi.string(lib._NAMESPACE).decode('ascii')
_T_PUBLICKEY = f'{_LIB_NAMESPACE}crypto_publickey'
_T_SECRETKEY = f'{_LIB_NAMESPACE}crypto_secretkey'
_T_SIGNATURE = f'{_LIB_NAMESPACE}crypto_signature'

_crypto_sign_keypair = getattr(lib, f'{_LIB_NAMESPACE}crypto_sign_keypair')
_crypto_sign_signature = getattr(lib, f'{_LIB_NAMESPACE}crypto_sign_signature')
_crypto_sign_verify = getattr(lib, f'{_LIB_NAMESPACE}crypto_sign_verify')


def keypair():
	_pk = ffi.new(_T_PUBLICKEY)
	_sk = ffi.new(_T_SECRETKEY)

	errno = _crypto_sign_keypair(_pk, _sk)

	if errno == 0:
		return bytes(_pk), bytes(_sk)
	raise RuntimeError(f'{_crypto_sign_keypair.__name__} returned error code {errno}')


def sign(m, sk):
	_m = ffi.from_buffer(m)
	_sk = ffi.cast(_T_SECRETKEY, ffi.from_buffer(sk))
	_sigbuf = ffi.new(_T_SIGNATURE)
	_siglen = ffi.new('size_t*')

	errno = _crypto_sign_signature(_sigbuf, _siglen, _m, len(m), _sk)

	if errno == 0:
		_sig = _sigbuf[0 : _siglen[0]]  # Variable-length signature
		return bytes(_sig)
	raise RuntimeError(f'{_crypto_sign_signature.__name__} returned error code {errno}')


def verify(sig, m, pk):
	_sig = ffi.from_buffer(sig)
	_m = ffi.from_buffer(m)
	_pk = ffi.cast(_T_PUBLICKEY, ffi.from_buffer(pk))

	errno = _crypto_sign_verify(_sig, len(_sig), _m, len(_m), _pk)

	if errno == 0:
		return
	if errno == -1:
		raise ValueError('verification failed')
	raise RuntimeError(f'{_crypto_sign_verify.__name__} returned error code {errno}')
