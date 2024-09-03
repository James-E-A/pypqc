# AUTOMATICALLY GENERATED FILE.
# RUN make.py IN THE PARENT MONOREPO TO REGENERATE THIS FILE.

from pqc._lib.kem_mceliece.libmceliece460896_clean import ffi, lib # TODO add optimized implementations


def keypair():
	with ffi.new('CRYPTO_PUBLICKEYBYTES_t') as pk,\
	     ffi.new('CRYPTO_SECRETKEYBYTES_t') as sk:
		errno = lib.crypto_kem_keypair(pk, sk)
		if errno == 0:
			return bytes(pk), bytes(sk)
		else:
			raise RuntimeError


def encap(pk_bytes):
	with ffi.new('CRYPTO_CIPHERTEXTBYTES_t') as c,\
	     ffi.new('CRYPTO_BYTES_t') as key,\
	     ffi.from_buffer(pk_bytes) as pk: # FIXME validate length
		errno = lib.crypto_kem_enc(c, key, pk)
		if errno == 0:
			return bytes(c), bytes(key)
		else:
			raise RuntimeError


def decap(ct_bytes, sk_bytes):
	with ffi.new('CRYPTO_BYTES_t') as key,\
	     ffi.from_buffer(ct_bytes) as c,\
	     ffi.from_buffer(sk_bytes) as sk: # FIXME validate lengths
		errno = lib.crypto_kem_dec(key, c, sk)
		if errno == 0:
			return bytes(key)
		else:
			raise RuntimeError
