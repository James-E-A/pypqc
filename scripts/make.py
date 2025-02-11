#!/usr/bin/env python3
#
#   CFFI module build script for PQClean C API
#
#  Part of the PyPQC bindings project
#
#  Originally written by: James Edington Administator
#
#  SPDX-License-Identifier: MIT OR Apache-2.0
#

from pathlib import Path
import re
from string import Template

from distutils.sysconfig import parse_makefile  # https://pypi.org/project/setuptools/

PARENT_PACKAGENAME = "pqc"

DIR = Path(__file__).parent
REPO = DIR / ".."
ASSETS = DIR / "assets"

COMMON_INCLUDES = ['fips202', 'randombytes', 'compat', 'crypto_declassify', 'sha2'] # FIXME tailor this per-library

PQCLEAN = REPO / 'PQClean'
assert PQCLEAN.is_dir()


for p1 in PQCLEAN.glob("crypto_*"):
	alg_type = re.match(r"crypto_(.*)", p1.name).group(1)

	for p2 in p1.iterdir():
		alg_commonname = re.match(r"(?:ml-)?\w*?(?=-|\d)", p2.name).group(0)
		alg_commonname_import = alg_commonname.replace('-', '_')

		package_suffix = {  # FIXME?
			'mceliece': 'libre',
			'ml-kem': 'kyber',
			'ml-dsa': 'libre',
			'sphincs': 'libre',
		}.get(alg_commonname, alg_commonname)

		package_dir = Path(REPO / 'projects' / f'pypqc-cffi-bindings-{package_suffix}')
		(package_dir / 'cffi_modules').rmdir()
		(package_dir / 'cffi_modules' / f"{libname_import}.py").write_text(cffi_module_src)

		for p3 in [p2 / 'clean']: # FIXME

			libname = Path(parse_makefile(p3 / 'Makefile')['LIB']).stem
			libname_import = libname.replace('-', '_')

			cffi_module_src = Template(
			  (ASSETS / "cffi.py-in.txt").read_text()
			).substitute({
			  'impl_dir_rel_str_repr': repr(p3.relative_to(REPO).as_posix()),
			  'parent_packagename_repr': repr(f"{PARENT_PACKAGENAME}._lib"),
			  'common_includes_repr': repr(COMMON_INCLUDES)
			})

			src = Template(
			  (ASSETS / f'{alg_type}.py-in.txt').read_text()
			).substitute({
			  'alg_prefix_import': alg_commonname_import,
			  'alg_lib_name': libname,
			  'alg_lib_name_import': libname_import
			})


