# https://foss.heptapod.net/pypy/cffi/-/issues/441
# https://github.com/pypa/setuptools/issues/1040

from setuptools import setup
from distutils.command.build_ext import build_ext as _build_ext
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel


class build_ext(_build_ext):
    """https://github.com/joerick/python-ctypes-package-sample/blob/7db688cd6ee32ae95bce0f75fb7d806926e20252/setup.py#L11"""
    def build_extension(self, ext):
        self._ctypes = isinstance(ext, CTypesExtension)
        return super().build_extension(ext)

    def get_export_symbols(self, ext):
        if self._ctypes:
            return ext.export_symbols
        return super().get_export_symbols(ext)

    def get_ext_filename(self, ext_name):
        if self._ctypes:
            return ext_name + ".so"
        return super().get_ext_filename(ext_name)


class bdist_wheel_abi_none(_bdist_wheel):
    """https://github.com/joerick/python-ctypes-package-sample/blob/7db688cd6ee32ae95bce0f75fb7d806926e20252/setup.py#L29"""
    def finalize_options(self):
        _bdist_wheel.finalize_options(self)
        self.root_is_pure = False

    def get_tag(self):
        python, abi, plat = _bdist_wheel.get_tag(self)
        return "py3", "none", plat


setup(
    cmdclass={"build_ext": build_ext, "bdist_wheel": bdist_wheel_abi_none},
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
