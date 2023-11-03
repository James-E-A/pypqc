from functools import partial

from .._impl_extern import shake256, PQCLEAN_randombytes
from . import _mceliece6960119

for module in [_mceliece6960119]:
	module.ffi.def_extern(name="shake256")(partial(shake256, ffi=module.ffi))
	module.ffi.def_extern(name="PQCLEAN_randombytes")(partial(PQCLEAN_randombytes, ffi=module.ffi))
