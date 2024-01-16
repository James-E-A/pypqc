from ._common_cffi_maker import make_pqclean_ffi
from textwrap import dedent

def make_kem_ffi(build_root, extra_cdefs=frozenset(), extra_c_header_sources=frozenset(), **k):
	cdefs = [dedent("""\
	// Public KEM interface
	static const char %(namespace)sCRYPTO_ALGNAME[...];
	int %(namespace)scrypto_kem_keypair(uint8_t *pk, uint8_t *sk);
	int %(namespace)scrypto_kem_enc(uint8_t *c, uint8_t *key, const uint8_t *pk);
	int %(namespace)scrypto_kem_dec(uint8_t *key, const uint8_t *c, const uint8_t *sk);
	#define %(namespace)sCRYPTO_SECRETKEYBYTES ...
	#define %(namespace)sCRYPTO_PUBLICKEYBYTES ...
	#define %(namespace)sCRYPTO_BYTES ...
	#define %(namespace)sCRYPTO_CIPHERTEXTBYTES ...
	""")]

	c_header_sources = [dedent("""\
	// Public KEM interface
	#include "api.h"
	""")]

	cdefs.append(dedent("""\
	// Site interface
	static const char _NAMESPACE[...];
	typedef uint8_t %(namespace)scrypto_secretkey[...];
	typedef uint8_t %(namespace)scrypto_publickey[...];
	typedef uint8_t %(namespace)scrypto_kem_plaintext[...];
	typedef uint8_t %(namespace)scrypto_kem_ciphertext[...];
	"""))

	c_header_sources.append(dedent("""\
	// Site interface
	static const char _NAMESPACE[] = "%(namespace)s";
	typedef uint8_t %(namespace)scrypto_secretkey[%(namespace)sCRYPTO_SECRETKEYBYTES];
	typedef uint8_t %(namespace)scrypto_publickey[%(namespace)sCRYPTO_PUBLICKEYBYTES];
	typedef uint8_t %(namespace)scrypto_kem_plaintext[%(namespace)sCRYPTO_BYTES];
	typedef uint8_t %(namespace)scrypto_kem_ciphertext[%(namespace)sCRYPTO_CIPHERTEXTBYTES];
	"""))

	cdefs.extend(extra_cdefs)
	c_header_sources.extend(extra_c_header_sources)

	return make_pqclean_ffi(build_root=build_root, c_header_sources=c_header_sources, cdefs=cdefs, **k)
