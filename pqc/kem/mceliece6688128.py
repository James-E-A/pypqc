from functools import partial

from .._impl_extern import _impl_shake256, _impl_randombytes
from .._util import using_avx2

if using_avx2():
	from ._mceliece6688128_avx2 import ffi, lib
else:
	from ._mceliece6688128 import ffi, lib

__all__ = ['kem_keypair', 'kem_enc', 'kem_dec']

ffi.def_extern(name='shake256')(partial(_impl_shake256, ffi=ffi))
ffi.def_extern(name='PQCLEAN_randombytes')(partial(_impl_randombytes, ffi=ffi))

_NAMESPACE = ffi.string(lib._NAMESPACE).decode('ascii')
_T_PUBLICKEY = f'_{_NAMESPACE}CRYPTO_PUBLICKEY'
_T_SECRETKEY = f'_{_NAMESPACE}CRYPTO_SECRETKEY'
_T_KEM_PLAINTEXT = f'_{_NAMESPACE}CRYPTO_KEM_PLAINTEXT'
_T_KEM_CIPHERTEXT = f'_{_NAMESPACE}CRYPTO_KEM_CIPHERTEXT'

_crypto_kem_keypair = getattr(lib, f'{_NAMESPACE}crypto_kem_keypair')
_crypto_kem_enc = getattr(lib, f'{_NAMESPACE}crypto_kem_enc')
_crypto_kem_dec = getattr(lib, f'{_NAMESPACE}crypto_kem_dec')


def kem_keypair():
	pk = ffi.new(_T_PUBLICKEY)
	sk = ffi.new(_T_SECRETKEY)

	errno = _crypto_kem_keypair(ffi.cast('char*', pk), ffi.cast('char*', sk))

	if errno:
		raise RuntimeError(f"{_NAMESPACE}crypto_kem_keypair returned error code {errno}")
	return bytes(pk), bytes(sk)


def kem_enc(pk):
	ciphertext = ffi.new(_T_KEM_CIPHERTEXT)
	key = ffi.new(_T_KEM_PLAINTEXT)
	pk = ffi.cast(_T_PUBLICKEY, ffi.from_buffer(pk))

	errno = _crypto_kem_enc(ffi.cast('char*', ciphertext), ffi.cast('char*', key), ffi.cast('char*', pk))

	if errno:
		raise RuntimeError(f"{_NAMESPACE}crypto_kem_enc returned error code {errno}")

	return bytes(key), bytes(ciphertext)


def kem_dec(ciphertext, sk):
	key = ffi.new(_T_KEM_PLAINTEXT)
	ciphertext = ffi.cast(_T_KEM_CIPHERTEXT, ffi.from_buffer(ciphertext))
	sk = ffi.cast(_T_SECRETKEY, ffi.from_buffer(sk))

	errno = _crypto_kem_dec(ffi.cast('char*', key), ffi.cast('char*', ciphertext), ffi.cast('char*', sk))

	if errno:
		raise RuntimeError(f"{_NAMESPACE}crypto_kem_dec returned error code {errno}")

	return bytes(key)

