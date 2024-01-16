from ._sign_cffi_maker import make_sign_ffi
from textwrap import dedent
import re

def make_falcon_ffi(build_root):
	common_sources = ['fips202.c', 'randombytes.c']

	patent_info = (
		2,
                ['US7308097B2'], [
		'https://csrc.nist.gov/csrc/media/Projects/post-quantum-cryptography/documents/selected-algos-2022/final-ip-statements/Falcon-Statements-final.pdf#page=20']
	)

	return make_sign_ffi(build_root=build_root, common_sources=common_sources, patent_info=patent_info)
