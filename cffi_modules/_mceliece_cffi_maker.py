from ._common_cffi_maker import make_pqclean_ffi
from textwrap import dedent

def make_mceliece_ffi(build_root):
	cdefs = []
	c_header_sources = []
	common_sources = ['fips202.c', 'randombytes.c']

	cdefs.append(dedent("""\
	// Public KEM interface
	static const char %(namespace)sCRYPTO_ALGNAME[...];
	int %(namespace)scrypto_kem_keypair(unsigned char *pk, unsigned char *sk);
	int %(namespace)scrypto_kem_enc(unsigned char *c, unsigned char *key, const unsigned char *pk);
	int %(namespace)scrypto_kem_dec(unsigned char *key, const unsigned char *c, const unsigned char *sk);
	"""))

	c_header_sources.append(dedent("""\
	// Public KEM interface
	#include "api.h"
	"""))

	cdefs.append(dedent("""\
	// Exposed internal interface
	typedef ... gf;
	int %(namespace)spk_gen(unsigned char *pk, unsigned char *sk, const uint32_t *perm, int16_t *pi, uint64_t *pivots);
	void %(namespace)sencrypt(unsigned char *s, const unsigned char *pk, unsigned char *e);
	int %(namespace)sdecrypt(unsigned char *e, const unsigned char *sk, const unsigned char *c);
	int %(namespace)sgenpoly_gen(gf *out, gf *f);
	#define SYS_N ...
	#define SYS_T ...
	#define GFBITS ...
	#define SYND_BYTES ...
	"""))

	c_header_sources.append(dedent("""\
	// Exposed internal interface
	#include "encrypt.h"
	#include "decrypt.h"
	#include "params.h"
	#include "sk_gen.h"
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
