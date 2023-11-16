from functools import partial
from importlib import import_module

from .._impl_extern import _impl_shake256, _impl_randombytes


__all__ = [
	'mceliece348864',
	'mceliece460896',
	'mceliece6688128',
	'mceliece6960119',
	'mceliece8192128']


class _McElieceKEM:
	# This being a Python "class" is NOT an API guarantee.
	# These could be re-factored out into file-level modules in the future.

	def kem_keypair(self):
		ffi = self._ffi
		pk = ffi.new(self.__T_PUBLICKEY)
		sk = ffi.new(self.__T_SECRETKEY)
		err = self.__crypto_kem_keypair(ffi.cast('char*', pk), ffi.cast('char*', sk))
		if err:
			raise RuntimeError(f"{self.__NAMESPACE}crypto_kem_keypair returned error code {err}")
		return bytes(pk), bytes(sk)

	def kem_enc(self, pk):
		ffi = self._ffi
		ciphertext = ffi.new(self.__T_KEM_CIPHERTEXT)
		key = ffi.new(self.__T_KEM_PLAINTEXT)
		pk = ffi.cast(self.__T_PUBLICKEY, ffi.from_buffer(pk))
		err = self.__crypto_kem_enc(ffi.cast('char*', ciphertext), ffi.cast('char*', key), ffi.cast('char*', pk))
		if err:
			raise RuntimeError(f"{self.__NAMESPACE}crypto_kem_enc returned error code {err}")
		return bytes(key), bytes(ciphertext)

	def kem_dec(self, ciphertext, sk):
		ffi = self._ffi
		key = ffi.new(self.__T_KEM_PLAINTEXT)
		ciphertext = ffi.cast(self.__T_KEM_CIPHERTEXT, ffi.from_buffer(ciphertext))
		sk = ffi.cast(self.__T_SECRETKEY, ffi.from_buffer(sk))
		err = self.__crypto_kem_dec(ffi.cast('char*', key), ffi.cast('char*', ciphertext), ffi.cast('char*', sk))
		if err:
			raise RuntimeError(f"{self.__NAMESPACE}crypto_kem_dec returned error code {err}")
		return bytes(key)

	def __init__(self, cffi_module):
		self._ffi = ffi = cffi_module.ffi
		self._lib = lib = cffi_module.lib

		ffi.def_extern(name="shake256")(partial(_impl_shake256, ffi=ffi))
		ffi.def_extern(name="PQCLEAN_randombytes")(partial(_impl_randombytes, ffi=ffi))

		self.__NAMESPACE = NAMESPACE = ffi.string(lib._NAMESPACE).decode('ascii')
		self.__T_PUBLICKEY = f'_{NAMESPACE}CRYPTO_PUBLICKEY'
		self.__T_SECRETKEY = f'_{NAMESPACE}CRYPTO_SECRETKEY'
		self.__T_KEM_PLAINTEXT = f'_{NAMESPACE}CRYPTO_KEM_PLAINTEXT'
		self.__T_KEM_CIPHERTEXT = f'_{NAMESPACE}CRYPTO_KEM_CIPHERTEXT'

		self.__crypto_kem_keypair = getattr(lib, f'{NAMESPACE}crypto_kem_keypair')
		self.__crypto_kem_enc = getattr(lib, f'{NAMESPACE}crypto_kem_enc')
		self.__crypto_kem_dec = getattr(lib, f'{NAMESPACE}crypto_kem_dec')


for module in __all__:
	cffi_module = import_module(f"._{module}", package=__name__)
	globals()[module] = _McElieceKEM(cffi_module)
