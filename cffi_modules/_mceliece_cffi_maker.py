from ._kem_cffi_maker import make_kem_ffi
from textwrap import dedent

def make_mceliece_ffi(build_root):
	common_sources = ['fips202.c', 'randombytes.c']

	extra_cdefs = [dedent("""\
	// Exposed internal interface
	typedef ... gf;
	int pk_gen(uint8_t *pk, uint8_t *sk, const uint32_t *perm, int16_t *pi, uint64_t *pivots);
	void encrypt(uint8_t *s, const uint8_t *pk, uint8_t *e);
	int decrypt(uint8_t *e, const uint8_t *sk, const uint8_t *c);
	int genpoly_gen(gf *out, gf *f);
	#define SYS_N ...
	#define SYS_T ...
	#define GFBITS ...
	#define SYND_BYTES ...
	""")]

	extra_c_header_sources = [dedent("""\
	// Exposed internal interface
	#include "encrypt.h"
	#include "decrypt.h"
	#include "params.h"
	#include "sk_gen.h"
	#define pk_gen %(namespace)spk_gen
	#define encrypt %(namespace)sencrypt
	#define decrypt %(namespace)sdecrypt
	#define genpoly_gen %(namespace)sgenpoly_gen
	""")]

	return make_kem_ffi(build_root=build_root, extra_c_header_sources=extra_c_header_sources, extra_cdefs=extra_cdefs, common_sources=common_sources)
