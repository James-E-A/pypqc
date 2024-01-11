# https://foss.heptapod.net/pypy/cffi/-/issues/441
# https://github.com/pypa/setuptools/issues/1040

from setuptools import setup

setup(
    cffi_modules=[
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
