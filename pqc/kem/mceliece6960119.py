from . import _mceliece6960119
_ffi = _mceliece6960119.ffi

__all__ = ['kem_keypair', 'kem_enc', 'kem_dec']

_NAMESPACE = _ffi.string(_mceliece6960119.lib._NAMESPACE).decode('ascii')
_T_PUBLICKEY = f'_{_NAMESPACE}CRYPTO_PUBLICKEY'
_T_SECRETKEY = f'_{_NAMESPACE}CRYPTO_SECRETKEY'
_T_KEM_PLAINTEXT = f'_{_NAMESPACE}CRYPTO_KEM_PLAINTEXT'
_T_KEM_CIPHERTEXT = f'_{_NAMESPACE}CRYPTO_KEM_CIPHERTEXT'
_pk_gen = getattr(_mceliece6960119.lib, f'{_NAMESPACE}pk_gen')
_encrypt = getattr(_mceliece6960119.lib, f'{_NAMESPACE}encrypt')
_decrypt = getattr(_mceliece6960119.lib, f'{_NAMESPACE}decrypt')
_crypto_kem_keypair = getattr(_mceliece6960119.lib, f'{_NAMESPACE}crypto_kem_keypair')
_crypto_kem_enc = getattr(_mceliece6960119.lib, f'{_NAMESPACE}crypto_kem_enc')
_crypto_kem_dec = getattr(_mceliece6960119.lib, f'{_NAMESPACE}crypto_kem_dec')

def kem_keypair():
	pk = _ffi.new(_T_PUBLICKEY)
	sk = _ffi.new(_T_SECRETKEY)
	err = _crypto_kem_keypair(_ffi.cast('char*', pk), _ffi.cast('char*', sk))
	if err:
		raise RuntimeError(_crypto_kem_keypair)
	return bytes(pk), bytes(sk)

def kem_enc(pk):
	key = _ffi.new(_T_KEM_PLAINTEXT)
	ciphertext = _ffi.new(_T_KEM_CIPHERTEXT)
	pk = _ffi.cast(_T_PUBLICKEY, _ffi.from_buffer(pk))
	err = _crypto_kem_enc(_ffi.cast('char*', ciphertext), _ffi.cast('char*', key), _ffi.cast('char*', pk))
	if err:
		raise RuntimeError((err, _crypto_kem_enc))
	return bytes(key), bytes(ciphertext)

def kem_dec(ciphertext, sk):
	key = _ffi.new(_T_KEM_PLAINTEXT)
	ciphertext = _ffi.cast(_T_KEM_CIPHERTEXT, _ffi.from_buffer(ciphertext))
	sk = _ffi.cast(_T_SECRETKEY, _ffi.from_buffer(sk))
	err = _crypto_kem_dec(_ffi.cast('char*', key), _ffi.cast('char*', ciphertext), _ffi.cast('char*', sk))
	if err:
		raise RuntimeError((err, _crypto_kem_dec))
	return bytes(key)
