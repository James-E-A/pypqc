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

PQCLEAN = REPO / 'PQClean'
assert PQCLEAN.is_dir()


for p1 in PQCLEAN.glob("crypto_*"):
	alg_type = re.match(r"crypto_(.*)", p1.name).group(1)

	for p2 in p1.iterdir():
		alg_name_paramset, alg_name = re.match(r'^(((?:ml-|)[\w\-]+?)-?(?=\d|padded|shake|sha2)[\w\-]+)$', p2.name).groups()

		pypi_suffix = {  # FIXME?
			'mceliece': 'libre',
			'ml-kem': 'kyber',
			'ml-dsa': 'libre',
			'sphincs': 'libre'
		}.get(alg_name, alg_name)

		common_includes = ['fips202', 'randombytes', 'compat', 'crypto_declassify', 'sha2'] # FIXME!

		# The root of the PACKAGING directory for the package that INCLUDES this suite
		cur_bindings_package_dir = REPO / 'projects' / f'pypqc-cffi-bindings-{pypi_suffix}'
		cur_cffi_parentpackagname_arg = f"{PARENT_PACKAGENAME}._lib.{alg_type}_{alg_name.replace('-', '_')}"

		for p3 in [p2 / 'clean']: # FIXME
			alg_impl = p3.name

			libname = Path(parse_makefile(p3 / 'Makefile')['LIB']).stem

			cffi_module_src = Template(
			  (ASSETS / "cffi.py-in.txt").read_text()
			).substitute({
			  'impl_dir_rel_str_repr': repr(p3.relative_to(REPO).as_posix()),
			  'parent_packagename_repr': repr(cur_cffi_parentpackagname_arg),
			  'common_includes_repr': repr(common_includes),
			})

			(cur_bindings_package_dir / 'cffi_modules' / f"{libname.replace('-', '_')}.py").write_text(cffi_module_src)
			(cur_bindings_package_dir / 'src' / cur_cffi_parentpackagname_arg.replace('.', '/'))

			src = Template(
			  (ASSETS / f'{alg_type}.py-in.txt').read_text()
			).substitute({
			  'internal_lib_module': f"{cur_cffi_parentpackagname_arg}.{libname.replace('-', '_')}",
			  'alg_name': alg_name_paramset,
			})

		(REPO / 'projects' / 'pypqc' / 'src' / PARENT_PACKAGENAME / alg_type / f"{alg_name_paramset.replace('-', '_')}.py").write_text(src)
