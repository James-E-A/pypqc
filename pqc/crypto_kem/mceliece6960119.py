SYS_N = 6960
SYS_T = 119

from . import _mceliece6960119

def encrypt():
	print(_mceliece6960119.lib.encrypt)
