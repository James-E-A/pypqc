# AUTOMATICALLY GENERATED FILE.
# RUN make.py IN THE PARENT MONOREPO TO REGENERATE THIS FILE.

from pqc._lib.kem_mceliece.libmceliece348864_clean import ffi as _ffi, lib as _lib # TODO add optimized implementations


def keypair():
	with _ffi.new('CRYPTO_PUBLICKEYBYTES_t') as pk,\
	     _ffi.new('CRYPTO_SECRETKEYBYTES_t') as sk:
		errno = _lib.crypto_kem_keypair(pk, sk)
		if errno == 0:
			return bytes(pk), bytes(sk)
		else:
			raise RuntimeError


def encap(pk_bytes):
	with _ffi.new('CRYPTO_CIPHERTEXTBYTES_t') as c,\
	     _ffi.new('CRYPTO_BYTES_t') as key,\
	     _ffi.from_buffer(pk_bytes) as pk: # FIXME validate length
		errno = _lib.crypto_kem_enc(c, key, pk)
		if errno == 0:
			return bytes(c), bytes(key)
		else:
			raise RuntimeError


def decap(ct_bytes, sk_bytes):
	with _ffi.new('CRYPTO_BYTES_t') as key,\
	     _ffi.from_buffer(ct_bytes) as c,\
	     _ffi.from_buffer(sk_bytes) as sk: # FIXME validate lengths
		errno = _lib.crypto_kem_dec(key, c, sk)
		if errno == 0:
			return bytes(key)
		else:
			raise RuntimeError
