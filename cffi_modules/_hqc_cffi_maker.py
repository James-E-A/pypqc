from ._kem_cffi_maker import make_kem_ffi
from textwrap import dedent

def make_hqc_ffi(build_root):
	common_sources = ['fips202.c', 'randombytes.c']

	return make_kem_ffi(build_root=build_root, common_sources=common_sources)
