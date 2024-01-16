from ._common_cffi_maker import make_pqclean_ffi
from textwrap import dedent

def make_hqc_ffi(build_root):
	cdefs = []
	c_header_sources = []
	common_sources = ['fips202.c', 'randombytes.c']
	patent_info = (
		3, [
		'FR2956541B1/US9094189B2/EP2537284B1',], [
		'https://csrc.nist.gov/csrc/media/Projects/post-quantum-cryptography/documents/round-4/final-ip-statements/HQC-Statements-Round4.pdf']
	)

	cdefs.append(dedent("""\
	// Public KEM interface
	static const char %(namespace)sCRYPTO_ALGNAME[...];
	int %(namespace)scrypto_kem_keypair(uint8_t *pk, uint8_t *sk);
	int %(namespace)scrypto_kem_enc(uint8_t *c, uint8_t *key, const uint8_t *pk);
	int %(namespace)scrypto_kem_dec(uint8_t *key, const uint8_t *c, const uint8_t *sk);
	"""))

	c_header_sources.append(dedent("""\
	// Public KEM interface
	#include "api.h"
	"""))

	cdefs.append(dedent("""\
	// Exposed internal interface
	// ... TODO
	"""))

	c_header_sources.append(dedent("""\
	// Exposed internal interface
	// ... TODO
	"""))

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

	return make_pqclean_ffi(build_root=build_root, c_header_sources=c_header_sources, cdefs=cdefs, common_sources=common_sources)
