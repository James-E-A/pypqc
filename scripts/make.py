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


from pathlib import Path, PurePosixPath
import re
import string

from distutils.sysconfig import parse_makefile  # https://pypi.org/project/setuptools/


PARENT_PACKAGENAME = "pqc"
CFFI_PARENT_PACKAGENAME = f"{PARENT_PACKAGENAME}._lib"

REPO = Path(__file__).parent / '..'
PQCLEAN = REPO / 'lib' / 'PQClean'
assert PQCLEAN.is_dir()

COMMON_INCLUDES = [  # FIXME!
    'fips202',
    'randombytes',
    'compat',
    'crypto_declassify',
    'sha2'
]

PYPI_SUFFIX = {  # FIXME?
    "mceliece": "libre",
    "ml-dsa": "libre",
    "sphincs": "libre",
    "ml-kem": "kyber",
}

CFFI_MODULE_TEMPLATE = string.Template((Path(__file__).parent / 'cffi_module_template.txt').read_text())

SRC_TEMPLATES = {
	'kem': string.Template((Path(__file__).parent / 'api_kem_template.txt').read_text()),
	'sign': string.Template((Path(__file__).parent / 'api_sign_template.txt').read_text()),
	'varsign': string.Template((Path(__file__).parent / 'api_varsign_template.txt').read_text())
}


for p1 in PQCLEAN.glob("crypto_*"):
    alg_type = re.match(r"crypto_(.*)", p1.name).group(1)

    (REPO / 'projects' / 'pypqc' / 'src' / PARENT_PACKAGENAME  / alg_type).mkdir(exist_ok=True, parents=True)
    (REPO / 'projects' / 'pypqc' / 'src' / PARENT_PACKAGENAME  / alg_type / "__init__.py").open('a').close()

    for p2 in p1.iterdir():
        alg_name_paramset, alg_name = re.match(r'^(((?:ml-|)[\w\-]+?)-?(?=\d|padded|shake|sha2)[\w\-]+)$', p2.name).groups()

        pypy_listing = f"pypqc-cffi-bindings-{PYPI_SUFFIX.get(alg_name, alg_name)}"
        (REPO / 'projects' / pypy_listing / 'cffi_modules').mkdir(exist_ok=True)

        cffi_parentpackageleaf = f"{alg_type}_{alg_name.replace('-', '_')}"
        cffi_parentpackagename = f"{CFFI_PARENT_PACKAGENAME}.{cffi_parentpackageleaf}"

        for p3 in p2.iterdir():
            if not p3.is_dir():
                continue

            alg_impl = p3.name
            libname = PurePosixPath(parse_makefile(p3 / 'Makefile')['LIB']).stem
            cffi_packagename = f"{cffi_parentpackagename}.{libname.replace('-', '_')}"

            if alg_impl != 'clean':
                continue # FIXME

            src = SRC_TEMPLATES[
                alg_type
            ].substitute({
                'cffi_packagename': cffi_packagename
            })

            cffi_module_src = CFFI_MODULE_TEMPLATE.substitute({
                'impl_dir_rel_str_repr': repr(p3.relative_to(REPO).as_posix()),
                'parent_packagename_repr': repr(cffi_parentpackagename),
                'common_includes_repr': repr(COMMON_INCLUDES),
            })

            (REPO / 'projects' / pypy_listing / 'cffi_modules' / f"{libname}.py").write_text(cffi_module_src)
            (REPO / 'projects' / 'pypqc' / 'src' / PARENT_PACKAGENAME  / alg_type / f"{alg_name_paramset.replace('-', '_')}.py").write_text(src)
            
