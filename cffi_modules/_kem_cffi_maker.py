from ._common_cffi_maker import make_pqclean_ffi
from textwrap import dedent

def make_kem_ffi(build_root, extra_cdefs=frozenset(), extra_c_header_sources=frozenset(), **k):
	cdefs = [dedent("""\
	// Public KEM interface
	int crypto_kem_keypair(uint8_t *pk, uint8_t *sk);
	int crypto_kem_enc(uint8_t *c, uint8_t *key, const uint8_t *pk);
	int crypto_kem_dec(uint8_t *key, const uint8_t *c, const uint8_t *sk);
	""")]

	c_header_sources = [dedent("""\
	// Public KEM interface
	#include "api.h"
	#define crypto_kem_keypair %(namespace)scrypto_kem_keypair
	#define crypto_kem_enc %(namespace)scrypto_kem_enc
	#define crypto_kem_dec %(namespace)scrypto_kem_dec
	""")]

	cdefs.append(dedent("""\
	// Site interface
	typedef uint8_t _CRYPTO_SECRETKEY_t[...];
	typedef uint8_t _CRYPTO_PUBLICKEY_t[...];
	typedef uint8_t _CRYPTO_KEM_PLAINTEXT_t[...];
	typedef uint8_t _CRYPTO_KEM_CIPHERTEXT_t[...];
	"""))

	c_header_sources.append(dedent("""\
	// Site interface
	typedef uint8_t _CRYPTO_SECRETKEY_t[%(namespace)sCRYPTO_SECRETKEYBYTES];
	typedef uint8_t _CRYPTO_PUBLICKEY_t[%(namespace)sCRYPTO_PUBLICKEYBYTES];
	typedef uint8_t _CRYPTO_KEM_PLAINTEXT_t[%(namespace)sCRYPTO_BYTES];
	typedef uint8_t _CRYPTO_KEM_CIPHERTEXT_t[%(namespace)sCRYPTO_CIPHERTEXTBYTES];
	"""))

	cdefs.extend(extra_cdefs)
	c_header_sources.extend(extra_c_header_sources)

	return make_pqclean_ffi(build_root=build_root, c_header_sources=c_header_sources, cdefs=cdefs, **k)
