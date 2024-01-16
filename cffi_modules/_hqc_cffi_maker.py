from ._kem_cffi_maker import make_kem_ffi
from textwrap import dedent

def make_hqc_ffi(build_root):
	common_sources = ['fips202.c', 'randombytes.c']

	patent_info = (
		3, [
		'FR2956541B1/US9094189B2/EP2537284B1',], [
		'https://csrc.nist.gov/csrc/media/Projects/post-quantum-cryptography/documents/round-4/final-ip-statements/HQC-Statements-Round4.pdf']
	)

	return make_kem_ffi(build_root=build_root, common_sources=common_sources, patent_info=patent_info)
