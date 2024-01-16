from ._sign_cffi_maker import make_sign_ffi
from textwrap import dedent
import re

def make_sphincs_ffi(build_root):
	_hash_name = re.match(r'.*sphincs-(\w+)', str(build_root)).group(1)
	_hash_src = {'sha2': 'sha2.c', 'shake': 'fips202.c'}[_hash_name]
	common_sources = ['randombytes.c', _hash_src]

	return make_sign_ffi(build_root=build_root, common_sources=common_sources)
