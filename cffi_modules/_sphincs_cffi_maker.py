from ._common_cffi_maker import make_pqclean_ffi
from textwrap import dedent
import re

def make_sphincs_ffi(build_root):
	cdefs = []
	c_header_sources = []
	_hash_name = re.match(r'.*sphincs-(\w+)', str(build_root)).group(1)
	_hash_src = {'sha2': 'sha2.c', 'shake': 'fips202.c'}[_hash_name]
	common_sources = ['fips202.c', 'randombytes.c', _hash_src]

	cdefs.append(dedent("""\
	// Public signature interface
	static const char %(namespace)sCRYPTO_ALGNAME[...];
	int %(namespace)scrypto_sign_keypair(uint8_t *pk, uint8_t *sk);
	int %(namespace)scrypto_sign_signature(uint8_t *sig, size_t *siglen, const uint8_t *m, size_t mlen, const uint8_t *sk);
	int %(namespace)scrypto_sign_verify(const uint8_t *sig, size_t siglen, const uint8_t *m, size_t mlen, const uint8_t *pk);
	int %(namespace)scrypto_sign(uint8_t *sm, size_t *smlen, const uint8_t *m, size_t mlen, const uint8_t *sk);
	int %(namespace)scrypto_sign_open(uint8_t *m, size_t *mlen, const uint8_t *sm, size_t smlen, const uint8_t *pk);
	"""))

	c_header_sources.append(dedent("""\
	// Public signature interface
	#include "api.h"
	"""))

	cdefs.append(dedent(f"""\
	// Exposed internal interface
	// ... TODO
	"""))

	c_header_sources.append(dedent("""\
	// Exposed internal interface
	// ... TODO
	"""))

	cdefs.append(dedent(f"""\
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

	return make_pqclean_ffi(build_root=build_root, c_header_sources=c_header_sources, cdefs=cdefs, common_sources=common_sources)
