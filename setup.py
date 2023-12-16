from setuptools import setup, Extension

# TODO allow editable install?
# https://github.com/pypa/setuptools/issues/1040
# I'm not sure if "cffi_modules" supports deferring generation of C sources
# to compile-time...

setup(
    cffi_modules=[
        'cffi_modules/mceliece348864f_clean.py:ffi',
        'cffi_modules/mceliece460896f_clean.py:ffi',
        'cffi_modules/mceliece6688128f_clean.py:ffi',
        'cffi_modules/mceliece6960119f_clean.py:ffi',
        'cffi_modules/mceliece8192128f_clean.py:ffi',
    ],
)
