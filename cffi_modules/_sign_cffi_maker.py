from ._common_cffi_maker import make_pqclean_ffi
from textwrap import dedent

def make_sign_ffi(build_root, extra_c_header_sources=frozenset(), extra_cdefs=frozenset(), **k):
	cdefs = [dedent("""\
	// Public signature interface
	int crypto_sign_keypair(uint8_t *pk, uint8_t *sk);
	int crypto_sign_signature(uint8_t *sig, size_t *siglen, const uint8_t *m, size_t mlen, const uint8_t *sk);
	int crypto_sign_verify(const uint8_t *sig, size_t siglen, const uint8_t *m, size_t mlen, const uint8_t *pk);
	int crypto_sign(uint8_t *sm, size_t *smlen, const uint8_t *m, size_t mlen, const uint8_t *sk);
	int crypto_sign_open(uint8_t *m, size_t *mlen, const uint8_t *sm, size_t smlen, const uint8_t *pk);
	""")]

	c_header_sources = [dedent("""\
	// Public signature interface
	#include "api.h"
	#define crypto_sign_keypair %(namespace)scrypto_sign_keypair
	#define crypto_sign_signature %(namespace)scrypto_sign_signature
	#define crypto_sign_verify %(namespace)scrypto_sign_verify
	#define crypto_sign %(namespace)scrypto_sign
	#define crypto_sign_open %(namespace)scrypto_sign_open
	""")]

	cdefs.append(dedent("""\
	// Site interface
	typedef uint8_t _CRYPTO_SECRETKEY_t[...];
	typedef uint8_t _CRYPTO_PUBLICKEY_t[...];
	typedef uint8_t _CRYPTO_SIGNATURE_t[...];
	"""))

	c_header_sources.append(dedent("""\
	// Site interface
	typedef uint8_t _CRYPTO_SECRETKEY_t[%(namespace)sCRYPTO_SECRETKEYBYTES];
	typedef uint8_t _CRYPTO_PUBLICKEY_t[%(namespace)sCRYPTO_PUBLICKEYBYTES];
	typedef uint8_t _CRYPTO_SIGNATURE_t[%(namespace)sCRYPTO_BYTES];
	"""))

	cdefs.extend(extra_cdefs)
	c_header_sources.extend(extra_c_header_sources)

	return make_pqclean_ffi(build_root=build_root, c_header_sources=c_header_sources, cdefs=cdefs, **k)
