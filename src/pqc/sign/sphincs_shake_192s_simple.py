from .._lib.libsphincs_shake_192s_simple_clean import ffi, lib

__all__ = ['keypair', 'signature', 'verify']

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

	if errno:
		raise RuntimeError(f"{_LIB_NAMESPACE}crypto_sign_keypair returned error code {errno}")
	return bytes(_pk), bytes(_sk)


def signature(m, sk):
	_m = ffi.from_buffer(m)

	_sk = ffi.cast(_T_SECRETKEY, ffi.from_buffer(sk))
	assert len(_sk) == len(sk)

	_sig = ffi.new(_T_SIGNATURE)
	_siglen = ffi.new('size_t*')

	errno = _crypto_sign_signature(_sig, _siglen, _m, len(m), _sk)
	assert len(_sig) == _siglen[0]  # This is a fixed parameter; WHY is it output??

	if errno:
		raise RuntimeError(f"{_LIB_NAMESPACE}crypto_sign_signature returned error code {errno}")

	return bytes(_sig)


def verify(sig, m, pk):
	_sig = ffi.cast(_T_SIGNATURE, ffi.from_buffer(sig))

	_m = ffi.from_buffer(m)

	_pk = ffi.cast(_T_PUBLICKEY, ffi.from_buffer(pk))

	errno = _crypto_sign_verify(_sig, len(_sig), _m, len(_m), _pk)

	if errno:
		if errno == -1:
			raise ValueError('verification failed')
		raise RuntimeError(f"{_LIB_NAMESPACE}crypto_sign_verify returned error code {errno}")

	return

