#!/usr/bin/env python3
#
#   Python CFFI module for PQClean C API
#
#  Part of the PyPQC bindings project
#
#  Originally written by: James Edington Administator
#
#  SPDX-License-Identifier: MIT OR Apache-2.0
#

# 1. PyPI imports

import cffi  # https://pypi.org/project/cffi/

from distutils.sysconfig import parse_makefile  # https://pypi.org/project/setuptools/


# 2. standard library imports

from collections import deque
from itertools import chain
import os
from pathlib import Path, PurePosixPath
import platform
import re


# 3. Constants

IMPL_DIR = Path('lib/PQClean/crypto_sign/sphincs-shake-128s-simple/clean')
PARENT_PACKAGENAME = 'pqc._lib.sign_sphincs'
COMMON_INCLUDES = ['fips202', 'randombytes', 'compat', 'crypto_declassify', 'sha2']  # TODO determine if we can ditch the common directory in favor of e.g. leaning on system libraries and/or Python builtins?

IS_WIN = platform.system() == 'Windows'
IS_MAC = platform.system() == 'Darwin'

ENTRYPOINT = IMPL_DIR / "api.h"
MAKEFILE = IMPL_DIR / ("Makefile.microsoft_nmake" if IS_WIN else "Makefile")
COMMON_DIR = IMPL_DIR / ".." / ".." / ".." / "common"

CDEF_RE = re.compile(r'(?ms)^(?:\w+ .*?;|#define \w+[^\S\n]+(?=\S)(?!").*?$)') # FIXME kludge
CDEF_DEFINE_RE = re.compile(r'(?<=^#define )(\w+) (.*)') # FIXME kludge


# 4. Internal Utility Functions

def map_immed(f, it, *, splat=False):
	deque((starmap if splat else map)(f, it), 0)

def pop_all(list_, indices):
	reversed(list(map(list_.pop, sorted(indices, reverse=True))))


# 5. Body

# * initialize
ffibuilder = cffi.FFI()
c_header_sources = [f'#include "{ENTRYPOINT.name}"']
cdefs = []
depends = []
sources = []
extra_objects = []
include_dirs = [IMPL_DIR]
libraries = []
kwextra = {'py_limited_api': True}

entrypoint_src = ENTRYPOINT.read_text()
makefile_parsed = parse_makefile(MAKEFILE)


# * arg module_name

libname = PurePosixPath(makefile_parsed['LIBRARY' if IS_WIN else 'LIB']).stem

namespace = re.search(r'(?m)^#define (\w+)CRYPTO_ALGNAME', entrypoint_src).group(1)
namespace_re = re.compile(rf'({re.escape(namespace)}(\w+))')
bytecount_re = re.compile(rf'(?m)^#define ({re.escape(namespace)}(\w+)BYTES)\s+(\d+)')


# * kwarg c_header_sources, kwarg cdefs

for cdef in (re.sub(CDEF_DEFINE_RE, "\\1 ...", m[0]) for m in re.finditer(CDEF_RE, entrypoint_src)):
	m = re.search(namespace_re, cdef)
	if m is None:
		assert "FALCONPADDED" in cdef
		continue

	cdefs.append(re.sub(namespace_re, "\\2", cdef))
	c_header_sources.append(f"#define {m[2]} {m[1]}")

for m in re.finditer(bytecount_re, entrypoint_src):
	longname, name, bytecount = m.groups()
	if name == "CRYPTO_":
		name = "CRYPTO_PLAINTEXT"
	cdefs.append(f"typedef uint8_t _{name}_t[...];")
	c_header_sources.append(f"typedef uint8_t _{name}_t[{bytecount}];")


# * kwarg sources, extra_objects

if 'SOURCES' in makefile_parsed:
	for source in (Path(IMPL_DIR, s.strip()) for s in makefile_parsed['SOURCES'].split()):

		if IS_WIN and source.suffix in {'.s', '.S', '.asm'}:
			extra_objects.append(source)
			continue

		sources.append(source)

elif 'OBJECTS' in makefile_parsed:
	for source in (p for s in makefile_parsed['OBJECTS'].split() for p in IMPL_DIR.glob( PurePosixPath(s.strip()).with_suffix('.*').name )):

		if source.suffix == '.h':
			depends.append(source)
			continue

		if IS_WIN and source.suffix in {'.s', '.S', '.asm'}:
			extra_objects.append(source)
			continue

		sources.append(source)

for internal_libname in COMMON_INCLUDES:
	for source in COMMON_DIR.glob(f'{internal_libname}*'):

		if source.suffix == '.h':
			depends.append(source)
			continue

		if IS_WIN and source.suffix in {'.s', '.S', '.asm'}:
			extra_objects.append(source)
			continue

		sources.append(source)


# * kwarg extra_compile_args

extra_compile_args = [s.strip() for s in makefile_parsed['CFLAGS'].split()]


# * workarounds

if libname.startswith('libmceliece'):
	# upstream testing infrastructure cruft
	pop_all(sources, [i for i, source in enumerate(sources) if source.stem.startswith('aes')])
	pop_all(depends, [i for i, source in enumerate(depends) if source.stem.startswith('aes')])

tmp = []
for i, arg in enumerate(extra_compile_args):
	if arg.startswith('-I'):
		include_dirs.append(IMPL_DIR / arg[2:])
		tmp.append(i)
	if arg.startswith('/I'):
		if len(arg) > 2:
			include_dirs.append(IMPL_DIR / arg[2:])
			tmp.append(i)
		else:
			include_dirs.append(IMPL_DIR / extra_compile_args[i+1])
			tmp.extend([i, i+1])
pop_all(extra_compile_args, tmp)

pop_all(extra_compile_args, [i for i, arg in enumerate(extra_compile_args) if arg.startswith('-Werror') or arg == '/WX'])

if IS_WIN:
	# https://foss.heptapod.net/pypy/cffi/-/issues/516
	# https://www.reddit.com/r/learnpython/comments/175js2u/def_extern_says_im_not_using_it_in_api_mode/
	# https://learn.microsoft.com/en-us/cpp/build/reference/tc-tp-tc-tp-specify-source-file-type?view=msvc-170
	extra_compile_args.append('/TC')

	# https://stackoverflow.com/questions/69900013/link-error-cannot-build-python-c-extension-in-windows
	# https://learn.microsoft.com/en-us/windows/win32/seccrypto/required-libraries
	libraries.append('Advapi32')

if IS_MAC:
	# https://developer.apple.com/documentation/xcode-release-notes/xcode-12-release-notes
	# https://github.com/actions/runner-images/issues/2440
	# https://github.com/actions/runner-images/blob/c60f54012ab18029c1efe8a74bca16ed89a25791/images/macos/toolsets/toolset-11.json#L3
	# https://github.com/actions/runner-images/issues/1938
	extra_compile_args.extend([
		'-Wno-error=implicit-function-declaration',
		'-Wno-error=macro-redefined',
	])


# * finalize

map_immed(ffibuilder.cdef, cdefs)

ffibuilder.set_source(
	f"{PARENT_PACKAGENAME}.{libname.replace('-', '_')}",
	"\n".join(c_header_sources),
	sources=[os.path.normpath(p.as_posix()) for p in sources],
	include_dirs=[os.path.normpath(p.as_posix()) for p in include_dirs],
	extra_objects=[os.path.normpath(p.as_posix()) for p in extra_objects],
	extra_compile_args=extra_compile_args,
	depends=[os.path.normpath(p.as_posix()) for p in depends],
	libraries=libraries,
	**kwextra
)

ffi = ffibuilder

if __name__ == '__main__':
	import sys
	ffi.compile(sys.argv[1], verbose=True)
