# AUTOMATICALLY GENERATED FILE.
# RUN make.py IN THE PARENT MONOREPO TO REGENERATE THIS FILE.

from pqc._lib.kem_hqc.libhqc_256_clean import ffi, lib # TODO add optimized implementations


def keypair():
	with ffi.new('uint8_t[]', lib.CRYPTO_PUBLICKEYBYTES) as pk,\
	     ffi.new('uint8_t[]', lib.CRYPTO_SECRETKEYBYTES) as sk:
		errno = lib.crypto_kem_keypair(pk, sk)
		if errno == 0:
			return bytes(pk), bytes(sk)
		else:
			raise RuntimeError


def encap(pk_bytes):
	with ffi.new('uint8_t[]', lib.CRYPTO_CIPHERTEXTBYTES) as c,\
	     ffi.new('uint8_t[]', lib.CRYPTO_BYTES) as key,\
	     ffi.from_buffer(pk_bytes) as pk: # FIXME validate length
		errno = lib.crypto_kem_enc(c, key, pk)
		if errno == 0:
			return bytes(c), bytes(key)
		else:
			raise RuntimeError


def decap(ct_bytes, sk_bytes):
	with ffi.new('uint8_t[]', lib.CRYPTO_BYTES) as key,\
	     ffi.from_buffer(ct_bytes) as c,\
	     ffi.from_buffer(sk_bytes) as sk: # FIXME validate lengths
		errno = lib.crypto_kem_dec(key, c, sk)
		if errno == 0:
			return bytes(key)
		else:
			raise RuntimeError
