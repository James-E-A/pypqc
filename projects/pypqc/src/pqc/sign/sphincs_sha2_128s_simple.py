# AUTOMATICALLY GENERATED FILE.
# RUN make.py IN THE PARENT MONOREPO TO REGENERATE THIS FILE.

from pqc._lib.sign_sphincs.libsphincs_sha2_128s_simple_clean import ffi as _ffi, lib as _lib # TODO add optimized implementations

def keypair():
	with _ffi.new('CRYPTO_PUBLICKEYBYTES_t') as pk,\
	     _ffi.new('CRYPTO_SECRETKEYBYTES_t') as sk:
		errno = _lib.crypto_sign_keypair(pk, sk)
		if errno == 0:
			return bytes(pk), bytes(sk)
		else:
			raise RuntimeError


def sign(message, sk_bytes):
	with _ffi.new('CRYPTO_BYTES_t') as sig,\
	     _ffi.new('size_t*') as siglen,\
	     _ffi.from_buffer(message) as m,\
	     _ffi.from_buffer(sk_bytes) as sk:
		errno = _lib.crypto_sign_signature(sig, siglen, m, len(m), sk)
		if errno == 0:
			return bytes(sig[0:siglen[0]])
		else:
			raise RuntimeError


def verify(signature, message, pk_bytes):
	with _ffi.from_buffer(signature) as sig,\
	     _ffi.from_buffer(message) as m,\
	     _ffi.from_buffer(pk_bytes) as pk:
		errno = _lib.crypto_sign_verify(sig, len(sig), m, len(m), pk)
		if errno == 0:
			return
		else:
			raise ValueError("signature failed to verify.")


def verify_bool(signature, message, pk_bytes):
	with _ffi.from_buffer(signature) as sig,\
	     _ffi.from_buffer(message) as m,\
	     _ffi.from_buffer(pk_bytes) as pk:
		errno = _lib.crypto_sign_verify(sig, len(sig), m, len(m), pk)
		return (errno == 0)
