from ._common_cffi_maker import make_pqclean_ffi
from textwrap import dedent

def make_sign_ffi(build_root, extra_c_header_sources=frozenset(), extra_cdefs=frozenset(), **k):
	cdefs = [dedent("""\
	// Public signature interface
	int %(namespace)scrypto_sign_keypair(uint8_t *pk, uint8_t *sk);
	int %(namespace)scrypto_sign_signature(uint8_t *sig, size_t *siglen, const uint8_t *m, size_t mlen, const uint8_t *sk);
	int %(namespace)scrypto_sign_verify(const uint8_t *sig, size_t siglen, const uint8_t *m, size_t mlen, const uint8_t *pk);
	int %(namespace)scrypto_sign(uint8_t *sm, size_t *smlen, const uint8_t *m, size_t mlen, const uint8_t *sk);
	int %(namespace)scrypto_sign_open(uint8_t *m, size_t *mlen, const uint8_t *sm, size_t smlen, const uint8_t *pk);
	#define %(namespace)sCRYPTO_SECRETKEYBYTES ...
	#define %(namespace)sCRYPTO_PUBLICKEYBYTES ...
	#define %(namespace)sCRYPTO_BYTES ...
	""")]

	c_header_sources = [dedent("""\
	// Public signature interface
	#include "api.h"
	""")]

	cdefs.append(dedent("""\
	// Site interface
	static const char _NAMESPACE[...];
	typedef uint8_t %(namespace)scrypto_secretkey[...];
	typedef uint8_t %(namespace)scrypto_publickey[...];
	typedef uint8_t %(namespace)scrypto_signature[...];
	"""))

	c_header_sources.append(dedent("""\
	// Site interface
	static const char _NAMESPACE[] = "%(namespace)s";
	typedef uint8_t %(namespace)scrypto_secretkey[%(namespace)sCRYPTO_SECRETKEYBYTES];
	typedef uint8_t %(namespace)scrypto_publickey[%(namespace)sCRYPTO_PUBLICKEYBYTES];
	typedef uint8_t %(namespace)scrypto_signature[%(namespace)sCRYPTO_BYTES];
	"""))

	cdefs.extend(extra_cdefs)
	c_header_sources.extend(extra_c_header_sources)

	return make_pqclean_ffi(build_root=build_root, c_header_sources=c_header_sources, cdefs=cdefs, **k)
