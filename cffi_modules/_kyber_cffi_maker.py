from ._kem_cffi_maker import make_kem_ffi
from textwrap import dedent

def make_kyber_ffi(build_root):
	common_sources = ['fips202.c', 'randombytes.c']

	extra_cdefs = [dedent("""\
	// Exposed internal interface
	void %(namespace)sindcpa_enc(uint8_t *c, const uint8_t *m, const uint8_t *pk, const uint8_t *coins);
	void %(namespace)sindcpa_dec(uint8_t *m, const uint8_t *c, const uint8_t *sk);
	""")]

	extra_c_header_sources = [dedent("""\
	// Exposed internal interface
	#include "indcpa.h"
	""")]

	return make_kem_ffi(build_root=build_root, extra_c_header_sources=extra_c_header_sources, extra_cdefs=extra_cdefs, common_sources=common_sources)
