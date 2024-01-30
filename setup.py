# https://foss.heptapod.net/pypy/cffi/-/issues/441
# https://github.com/pypa/setuptools/issues/1040

import platform
from setuptools import setup
import sys
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

# Pending https://hpyproject.org/
ABI3_EXCLUDE_IMPLEMENTATIONS = {
  'PyPy',  # https://github.com/orgs/pypy/discussions/4884#discussioncomment-8309845
}


class site_bdist_wheel(_bdist_wheel):
    """https://github.com/joerick/python-ctypes-package-sample/blob/7db688cd6ee32ae95bce0f75fb7d806926e20252/setup.py#L29"""

    def finalize_options(self):
        # https://github.com/pypa/wheel/blob/0.42.0/src/wheel/bdist_wheel.py#L244
        if (platform.python_implementation() not in ABI3_EXCLUDE_IMPLEMENTATIONS
            # https://github.com/pypa/wheel/blob/0.42.0/src/wheel/bdist_wheel.py#L267
            and (self.distribution.has_ext_modules() or self.distribution.has_c_libraries())
            # https://github.com/pypa/setuptools/blob/v69.0.3/setuptools/command/build_ext.py#L160
            and all(ext.py_limited_api for ext in self.distribution.ext_modules)
        ):
            self.py_limited_api = f'cp{sys.version_info.major}{sys.version_info.minor}' if platform.python_implementation() == 'CPython' else f'py{sys.version_info.major}{sys.version_info.minor}'
        super().finalize_options()

    def get_tag(self):
        python, abi, plat = _bdist_wheel.get_tag(self)
        #if self.py_limited_api and platform.python_implementation() not in ABI3_EXCLUDE_IMPLEMENTATIONS:
        #    python = f'cp{sys.version_info.major}' if platform.python_implementation() == 'CPython' else f'py{sys.version_info.major}'
        #    abi = f'abi{sys.version_info.major}'
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
