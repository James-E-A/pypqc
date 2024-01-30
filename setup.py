# https://foss.heptapod.net/pypy/cffi/-/issues/441
# https://github.com/pypa/setuptools/issues/1040

import platform
from setuptools import setup
import wheel.bdist_wheel as _mod_bdist_wheel
_mod_bdist_wheel.PY_LIMITED_API_PATTERN = r'(cp|py)\d'
_bdist_wheel = _mod_bdist_wheel.bdist_wheel


class site_bdist_wheel(_bdist_wheel):
    """https://github.com/joerick/python-ctypes-package-sample/blob/7db688cd6ee32ae95bce0f75fb7d806926e20252/setup.py#L29"""
    def finalize_options(self):
        _bdist_wheel.finalize_options(self)
        self.root_is_pure = False

    def get_tag(self):
        python, abi, plat = _bdist_wheel.get_tag(self)
        if self.py_limited_api and platform.python_implementation() not in {
            'PyPy',  # https://github.com/orgs/pypy/discussions/4884#discussioncomment-8309845
        }:
            python = f'py{sys.version_info.major}'
            abi = f'abi{sys.version_info.major}'
        if not self.py_limited_api and platform.python_implementation() in {'CPython'}:
            # https://github.com/python-cffi/cffi/blob/v1.16.0/src/cffi/setuptools_ext.py#L114
            import pprint; raise AssertionError(pprint.pformat((locals(),
                {'self.py_limited_api': self.py_limited_api, 'platform.python_implementation()': platform.python_implementation()})))
        return python, abi, plat


setup(
    cmdclass={"bdist_wheel": site_bdist_wheel},
    cffi_modules=[
        'cffi_modules/dilithium2_clean.py:ffi',
        'cffi_modules/dilithium3_clean.py:ffi',
        'cffi_modules/dilithium5_clean.py:ffi',
        'cffi_modules/falcon_512_clean.py:ffi',
        'cffi_modules/falcon_1024_clean.py:ffi',
        'cffi_modules/hqc_128_clean.py:ffi',
        'cffi_modules/hqc_192_clean.py:ffi',
        'cffi_modules/hqc_256_clean.py:ffi',
        'cffi_modules/kyber512_clean.py:ffi',
        'cffi_modules/kyber768_clean.py:ffi',
        'cffi_modules/kyber1024_clean.py:ffi',
        'cffi_modules/mceliece348864f_clean.py:ffi',
        'cffi_modules/mceliece460896f_clean.py:ffi',
        'cffi_modules/mceliece6688128f_clean.py:ffi',
        'cffi_modules/mceliece6960119f_clean.py:ffi',
        'cffi_modules/mceliece8192128f_clean.py:ffi',
#        'cffi_modules/mceliece6688128pcf_clean.py:ffi',
#        'cffi_modules/mceliece6960119pcf_clean.py:ffi',
#        'cffi_modules/mceliece8192128pcf_clean.py:ffi',
        'cffi_modules/sphincs-sha2-128f-simple_clean.py:ffi',
        'cffi_modules/sphincs-sha2-128s-simple_clean.py:ffi',
        'cffi_modules/sphincs-sha2-192f-simple_clean.py:ffi',
        'cffi_modules/sphincs-sha2-192s-simple_clean.py:ffi',
        'cffi_modules/sphincs-sha2-256f-simple_clean.py:ffi',
        'cffi_modules/sphincs-sha2-256s-simple_clean.py:ffi',
        'cffi_modules/sphincs-shake-128f-simple_clean.py:ffi',
        'cffi_modules/sphincs-shake-128s-simple_clean.py:ffi',
        'cffi_modules/sphincs-shake-192f-simple_clean.py:ffi',
        'cffi_modules/sphincs-shake-192s-simple_clean.py:ffi',
        'cffi_modules/sphincs-shake-256f-simple_clean.py:ffi',
        'cffi_modules/sphincs-shake-256s-simple_clean.py:ffi',
    ],
)
