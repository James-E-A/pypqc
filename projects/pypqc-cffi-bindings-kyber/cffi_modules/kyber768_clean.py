#!/usr/bin/env python3
"""AUTOMATICALLY GENERATED FILE.
RUN make.py IN THE PARENT MONOREPO TO REGENERATE THIS FILE.
"""

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
IMPL_DIR = Path('lib', 'PQClean', 'crypto_kem', 'kyber768', 'clean')
COMMON_DIR = IMPL_DIR / '..' / '..' / '..' / 'common'
PARENT_PACKAGENAME = 'pqc._lib.kem_kyber'
COMMON_INCLUDES = ['fips202', 'randombytes', 'compat', 'crypto_declassify', 'sha2']  # TODO determine if we can ditch the common directory in favor of e.g. leaning on system libraries?
IS_WIN = platform.system() == 'Windows'

# 4. Functions
def map_immed(f, it, *, splat=False):
	deque((starmap if splat else map)(f, it), 0)

# 5. Body
ffibuilder = cffi.FFI()

kwextra = {'py_limited_api': True}

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
namespace = re.search(r'(?m)^#define (\w+)CRYPTO_ALGNAME', api_src).group(1)
namespace_r = re.compile(rf'({re.escape(namespace)}(\w+))')
cdef_r = re.compile(r'(?ms)^(?:\w+ .*?;|#define \w+[^\S\n]+(?=\S)(?!").*?$)')
cdef_define_r = re.compile(r'(?<=^#define )(\w+) (.*)')
for cdef in (re.sub(cdef_define_r, "\\1 ...", m[0]) for m in re.finditer(cdef_r, api_src)):
	m = re.search(namespace_r, cdef)
	if not m:
		if 'PQCLEAN_FALCONPADDED' in cdef:
			continue
	cdefs.append(re.sub(namespace_r, "\\2", cdef))
	c_header_sources.append(f"#define {m[2]} {m[1]}")


# Add internal utility fixed-array types for pypqc
array_t_r = re.compile(rf'(?m)^#define ({re.escape(namespace)}(\w+BYTES))\s+(\d+)')
for m in re.finditer(array_t_r, api_src):
	cdefs.append(f"typedef uint8_t {m[2]}_t[...];")
	c_header_sources.append(f"typedef uint8_t {m[2]}_t[{m[1]}];")
	print(cdefs[-1])
	print(c_header_sources[-1])


if 'SOURCES' in makefile_parsed:
	for source in (Path(IMPL_DIR, s.strip()) for s in makefile_parsed['SOURCES'].split()):
		if IS_WIN and source.suffix in {'.s', '.S', '.asm'}:
			extra_objects.append(source)
		else:
			sources.append(source)

elif 'OBJECTS' in makefile_parsed:
	for source in chain.from_iterable(IMPL_DIR.glob(Path(s.strip()).with_suffix('.*').name) for s in makefile_parsed['OBJECTS'].split()):
		if source.suffix in {'.h'}:
			depends.append(source)
			continue
		if IS_WIN and source.suffix in {'.s', '.S', '.asm'}:
			extra_objects.append(source)
		else:
			sources.append(source)


for internal_libname in COMMON_INCLUDES:
	for source in COMMON_DIR.glob(f'{internal_libname}*'):
		if source.suffix in {'.h'}:
			depends.append(source)
			continue
		if IS_WIN and source.suffix in {'.s', '.S', '.asm'}:
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
	f'{PARENT_PACKAGENAME}.{libname.replace("-", "_")}',
	'\n'.join(c_header_sources),
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
