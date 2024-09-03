#!/usr/bin/env python3
# This should probably be converted into a Makefile

from collections import deque
from itertools import chain
from pathlib import Path
import platform
import re
import subprocess


def main():
	root = Path(__file__).parent.parent  # absolute path to monorepo root, may or may not equal cwd
	assert (root / 'lib' / 'PQClean').exists()
	for projdir in (root / 'projects').glob('pypqc-cffi-bindings*'):  # absolute path to "project" dir, may or may not equal cwd
		proj_packageroot = projdir / 'src'
		(projdir / 'cffi_modules').mkdir(exist_ok=True)

		proj_libdir = projdir / 'lib'
		if (proj_libdir.is_file() or not proj_libdir.exists()):
			if platform.system() == 'Windows':
				# Git failed to check out the symlink properly.
				# Known bug on Windows systems without Administrator access.
				# (Of course, "developer mode" is of little use as it requires Administrator access to enable in the first place!)
				# Polyfill the broken/missing checkout.
				proj_libdir.unlink(missing_ok=True)
				subprocess.check_call(["MKLINK", "/J", proj_libdir, Path('..', '..', 'lib')], shell=True, cwd=proj_libdir.parent)

		assert (proj_libdir / 'PQClean').exists()

		for alg_packagedir in (proj_packageroot / 'pqc' / '_lib').iterdir():
			package = f'pqc._lib.{alg_packagedir.name}'
			alg_type, alg_prefix = alg_packagedir.name.split('_')
			for alg_dir in ((projdir / 'lib' / 'PQClean'
							 / f'crypto_{alg_type}').glob(f'{alg_prefix}*')
			):
				(root / 'projects' / 'pypqc' / 'src' / 'pqc' / alg_type / f'{alg_dir.name.replace("-", "_")}.py').write_text(f"""\
# AUTOMATICALLY GENERATED FILE.
# RUN make.py IN THE PARENT MONOREPO TO REGENERATE THIS FILE.

from pqc._lib.kem_{alg_prefix}.lib{alg_dir.name.replace("-", "_")}_clean import ffi, lib # TODO add optimized implementations


def keypair():
	with ffi.new('CRYPTO_PUBLICKEYBYTES_t') as pk,\\
	     ffi.new('CRYPTO_SECRETKEYBYTES_t') as sk:
		errno = lib.crypto_kem_keypair(pk, sk)
		if errno == 0:
			return bytes(pk), bytes(sk)
		else:
			raise RuntimeError


def encap(pk_bytes):
	with ffi.new('CRYPTO_CIPHERTEXTBYTES_t') as c,\\
	     ffi.new('CRYPTO_BYTES_t') as key,\\
	     ffi.from_buffer(pk_bytes) as pk: # FIXME validate length
		errno = lib.crypto_kem_enc(c, key, pk)
		if errno == 0:
			return bytes(c), bytes(key)
		else:
			raise RuntimeError


def decap(ct_bytes, sk_bytes):
	with ffi.new('CRYPTO_BYTES_t') as key,\\
	     ffi.from_buffer(ct_bytes) as c,\\
	     ffi.from_buffer(sk_bytes) as sk: # FIXME validate lengths
		errno = lib.crypto_kem_dec(key, c, sk)
		if errno == 0:
			return bytes(key)
		else:
			raise RuntimeError
""" if alg_type == 'kem' else f"""\
# AUTOMATICALLY GENERATED FILE.
# RUN make.py IN THE PARENT MONOREPO TO REGENERATE THIS FILE.

from pqc._lib.sign_{alg_prefix}.lib{alg_dir.name.replace("-", "_")}_clean import ffi, lib # TODO add optimized implementations

def keypair():
	with ffi.new('CRYPTO_PUBLICKEYBYTES_t') as pk,\\
	     ffi.new('CRYPTO_SECRETKEYBYTES_t') as sk:
		errno = lib.crypto_sign_keypair(pk, sk)
		if errno == 0:
			return bytes(pk), bytes(sk)
		else:
			raise RuntimeError


def sign(message, sk_bytes):
	with ffi.new('CRYPTO_BYTES_t') as sig,\\
	     ffi.new('size_t*') as siglen,\\
	     ffi.from_buffer(message) as m,\\
	     ffi.from_buffer(sk_bytes) as sk:
		errno = lib.crypto_sign_signature(sig, siglen, m, len(m), sk)
		if errno == 0:
			return bytes(sig[0:siglen[0]])
		else:
			raise RuntimeError


def verify(signature, message, pk_bytes):
	with ffi.from_buffer(signature) as sig,\\
	     ffi.from_buffer(message) as m,\\
	     ffi.from_buffer(pk_bytes) as pk:
		errno = lib.crypto_sign_verify(sig, len(sig), m, len(m), pk)
		if errno == 0:
			return
		else:
			raise ValueError("signature failed to verify.")


def verify_bool(signature, message, pk_bytes):
	with ffi.from_buffer(signature) as sig,\\
	     ffi.from_buffer(message) as m,\\
	     ffi.from_buffer(pk_bytes) as pk:
		errno = lib.crypto_sign_verify(sig, len(sig), m, len(m), pk)
		return bool(-errno)
""" if alg_type == 'sign' else None)

				for alg_impl_dir in (p for p in alg_dir.iterdir() if p.is_dir()):  # absolute path to implementation directory
					if alg_impl_dir.name != 'clean':
						continue # FIXME

					common_includes = ['fips202', 'randombytes', 'compat', 'crypto_declassify', 'sha2'] # FIXME

					(projdir / 'cffi_modules' / f'{alg_dir.name}_{alg_impl_dir.name}.py').write_text(f"""\
#!/usr/bin/env python3
\"\"\"AUTOMATICALLY GENERATED FILE.
RUN make.py IN THE PARENT MONOREPO TO REGENERATE THIS FILE.
\"\"\"

# 1. PyPI imports
import cffi  # https://pypi.org/project/cffi/
from distutils.sysconfig import parse_makefile  # https://pypi.org/project/setuptools/

# 2. standard library imports
from collections import deque
from itertools import chain
from pathlib import Path
import platform
import re

# 3. Constants
IMPL_DIR = Path({', '.join(repr(s) for s in alg_impl_dir.relative_to(projdir).parts)})
COMMON_DIR = IMPL_DIR / '..' / '..' / '..' / 'common'
PARENT_PACKAGENAME = {repr('.'.join(s for s in alg_packagedir.relative_to(proj_packageroot).parts))}
COMMON_INCLUDES = {common_includes!r}  # TODO determine if we can ditch the common directory in favor of e.g. leaning on system libraries?
IS_WIN = platform.system() == 'Windows'

# 4. Functions
def map_immed(f, it, *, splat=False):
	deque((starmap if splat else map)(f, it), 0)

# 5. Body
ffibuilder = cffi.FFI()

kwextra = {{'py_limited_api': True}}

makefile_parsed = parse_makefile(IMPL_DIR / ('Makefile.microsoft_nmake' if IS_WIN else 'Makefile'))
libname = Path(makefile_parsed['LIBRARY' if IS_WIN else 'LIB']).stem

api_src = (IMPL_DIR / 'api.h').read_text()

c_header_sources = ['#include "api.h"']
cdefs = []
depends = []
sources = []
extra_objects = []
include_dirs = [IMPL_DIR]
libraries = []


# Strip off the PQCLEAN_FOO_ prefixes.
# We do this by cffi-cdef'ing the clean (prefix-free) function names,
# then c-define'ing the clean function name to transmute it to its prefixed version.
namespace = re.search(r'(?m)^#define (\\w+)CRYPTO_ALGNAME', api_src).group(1)
namespace_r = re.compile(rf'({{re.escape(namespace)}}(\\w+))')
cdef_r = re.compile(r'(?ms)^(?:\\w+ .*?;|#define \\w+[^\\S\\n]+(?=\\S)(?!").*?$)')
cdef_define_r = re.compile(r'(?<=^#define )(\\w+) (.*)')
for cdef in (re.sub(cdef_define_r, "\\\\1 ...", m[0]) for m in re.finditer(cdef_r, api_src)):
	m = re.search(namespace_r, cdef)
	if not m:
		if 'PQCLEAN_FALCONPADDED' in cdef:
			continue
	cdefs.append(re.sub(namespace_r, "\\\\2", cdef))
	c_header_sources.append(f"#define {{m[2]}} {{m[1]}}")


# Add internal utility fixed-array types for pypqc
array_t_r = re.compile(rf'(?m)^#define ({{re.escape(namespace)}}(\\w+BYTES))\\s+(\\d+)')
for m in re.finditer(array_t_r, api_src):
	cdefs.append(f"typedef uint8_t {{m[2]}}_t[...];")
	c_header_sources.append(f"typedef uint8_t {{m[2]}}_t[{{m[1]}}];")


if 'SOURCES' in makefile_parsed:
	for source in (Path(IMPL_DIR, s.strip()) for s in makefile_parsed['SOURCES'].split()):
		if IS_WIN and source.suffix in {{'.s', '.S', '.asm'}}:
			extra_objects.append(source)
		else:
			sources.append(source)

elif 'OBJECTS' in makefile_parsed:
	for source in chain.from_iterable(IMPL_DIR.glob(Path(s.strip()).with_suffix('.*').name) for s in makefile_parsed['OBJECTS'].split()):
		if source.suffix in {{'.h'}}:
			depends.append(source)
			continue
		if IS_WIN and source.suffix in {{'.s', '.S', '.asm'}}:
			extra_objects.append(source)
		else:
			sources.append(source)


for internal_libname in COMMON_INCLUDES:
	for source in COMMON_DIR.glob(f'{{internal_libname}}*'):
		if source.suffix in {{'.h'}}:
			depends.append(source)
			continue
		if IS_WIN and source.suffix in {{'.s', '.S', '.asm'}}:
			extra_objects.append(source)
		else:
			sources.append(source)


extra_compile_args = [s.strip() for s in makefile_parsed['CFLAGS'].split()]


# * ?????
if libname.startswith('libmceliece'):
	tmp = []
	for i, source in enumerate(sources):
		if source.stem.startswith('aes'):
			tmp.append(i)
	map_immed(sources.pop, reversed(sorted(tmp)))

	tmp = []
	for i, source in enumerate(depends):
		if source.stem.startswith('aes'):
			tmp.append(i)
	map_immed(depends.pop, reversed(sorted(tmp)))


# * Move "include" flags to setuptools
tmp = []
for i, arg in enumerate(extra_compile_args):
	if arg.startswith('-I'):
		include_dirs.append(IMPL_DIR / arg[2:])
		tmp.extend([i])
	if arg.startswith('/I'):
		include_dirs.append(IMPL_DIR / (arg[2:] if len(arg) > 2 else extra_compile_args[i+1]))
		tmp.extend([i, i+1])
map_immed(extra_compile_args.pop, reversed(sorted(tmp)))


# * FIXME is this a problem with PQClean, or with CFFI?
tmp = []
for i, arg in enumerate(extra_compile_args):
	if arg.startswith('-Werror'):
		tmp.extend([i])
	if arg == '/WX':
		tmp.extend([i])
map_immed(extra_compile_args.pop, reversed(sorted(tmp)))


# * Other Windows compiler fixes
if platform.system() == 'Windows':
	# https://foss.heptapod.net/pypy/cffi/-/issues/516
	# https://www.reddit.com/r/learnpython/comments/175js2u/def_extern_says_im_not_using_it_in_api_mode/
	# https://learn.microsoft.com/en-us/cpp/build/reference/tc-tp-tc-tp-specify-source-file-type?view=msvc-170
	extra_compile_args.append('/TC')

	# https://stackoverflow.com/questions/69900013/link-error-cannot-build-python-c-extension-in-windows
	# https://learn.microsoft.com/en-us/windows/win32/seccrypto/required-libraries
	libraries.append('Advapi32')


#import pprint; pprint.pprint(locals())
map_immed(ffibuilder.cdef, cdefs)
##map_immed(ffibuilder.include, ffi_includes)  # Not working -- https://github.com/python-cffi/cffi/issues/43
ffibuilder.set_source(
	f'{{PARENT_PACKAGENAME}}.{{libname.replace("-", "_")}}',
	'\\n'.join(c_header_sources),
	sources=[p.as_posix() for p in sources],
	include_dirs=[p.as_posix() for p in include_dirs],
	extra_objects=[p.as_posix() for p in extra_objects],
	extra_compile_args=extra_compile_args,
	depends=[p.as_posix() for p in depends],
	libraries=libraries,
	**kwextra
)

ffi = ffibuilder


if __name__ == '__main__':
	import sys
	ffi.compile(sys.argv[1], verbose=True)
""")



if __name__ == '__main__':
	main()
