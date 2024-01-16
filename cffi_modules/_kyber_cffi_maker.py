from ._kem_cffi_maker import make_kem_ffi
from textwrap import dedent

def make_kyber_ffi(build_root):
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

	extra_cdefs = [dedent("""\
	// Exposed internal interface
	void %(namespace)sindcpa_enc(uint8_t *c, const uint8_t *m, const uint8_t *pk, const uint8_t *coins);
	void %(namespace)sindcpa_dec(uint8_t *m, const uint8_t *c, const uint8_t *sk);
	""")]

	extra_c_header_sources = [dedent("""\
	// Exposed internal interface
	#include "indcpa.h"
	""")]

	return make_kem_ffi(build_root=build_root, extra_c_header_sources=extra_c_header_sources, extra_cdefs=extra_cdefs, common_sources=common_sources, patent_info=patent_info)
