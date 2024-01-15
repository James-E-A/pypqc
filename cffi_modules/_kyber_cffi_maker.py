from ._common_cffi_maker import make_pqclean_ffi
from textwrap import dedent

def make_kyber_ffi(build_root):
	cdefs = []
	c_header_sources = []
	common_sources = ['fips202.c', 'randombytes.c']

	patent_info = (
		1,[
		'FR2956541A1/US9094189B2/EP2537284B1',
		'US9246675/EP2837128B1',
		'potential unknown others'], [
		'https://ntruprime.cr.yp.to/faq.html',
		'https://csrc.nist.gov/csrc/media/Projects/post-quantum-cryptography/documents/selected-algos-2022/nist-pqc-license-summary-and-excerpts.pdf',
		'https://groups.google.com/a/list.nist.gov/g/pqc-forum/c/G0DoD7lkGPk/m/d7Zw0qhGBwAJ',
		'https://datatracker.ietf.org/meeting/116/proceedings#pquip:~:text=Patents%20and%20PQC',
		'https://mailarchive.ietf.org/arch/msg/pqc/MS92cuZkSRCDEjpPP90s2uAcRPo/']
	)

	cdefs.append(dedent("""\
	// Public KEM interface
	int %(namespace)scrypto_kem_keypair(uint8_t *pk, uint8_t *sk);
	int %(namespace)scrypto_kem_enc(uint8_t *ct, uint8_t *ss, const uint8_t *pk);
	int %(namespace)scrypto_kem_dec(uint8_t *ss, const uint8_t *ct, const uint8_t *sk);
	"""))

	c_header_sources.append(dedent("""\
	// Public KEM interface
	#include "api.h"
	"""))

	cdefs.append(dedent("""\
	// Exposed internal interface
	void %(namespace)sindcpa_enc(uint8_t *c, const uint8_t *m, const uint8_t *pk, const uint8_t *coins);
	void %(namespace)sindcpa_dec(uint8_t *m, const uint8_t *c, const uint8_t *sk);
	"""))

	c_header_sources.append(dedent("""\
	// Exposed internal interface
	#include "indcpa.h"
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

	return make_pqclean_ffi(build_root=build_root, c_header_sources=c_header_sources, cdefs=cdefs, common_sources=common_sources, patent_info=patent_info)
