from ._sign_cffi_maker import make_sign_ffi
from textwrap import dedent
import re

def make_falcon_ffi(build_root):
	common_sources = ['fips202.c', 'randombytes.c']

	return make_sign_ffi(build_root=build_root, common_sources=common_sources)
