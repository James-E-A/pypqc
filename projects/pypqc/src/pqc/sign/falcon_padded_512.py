#
#  Part of the PyPQC bindings project
#
#  Originally written by: James Edington Administator
#
#  SPDX-License-Identifier: MIT OR Apache-2.0
#

from pqc._lib.sign_falcon.libfalcon_padded_512_clean import ffi, lib

ffi_new_fast = ffi.new_allocator(should_clear_after_alloc=False)
crypto_sign_keypair = lib.crypto_sign_keypair
crypto_sign_signature = lib.crypto_sign_signature
crypto_sign_verify = lib.crypto_sign_verify

__all__ = ["keypair", "sign", "verify", "verify_bool"]


def keypair():
    with ffi_new_fast('_CRYPTO_PUBLICKEY_t') as pk,\
         ffi_new_fast('_CRYPTO_SECRETKEY_t') as sk:
        ret = crypto_sign_keypair(pk, sk)
        if ret == 0:
            return bytes(pk), bytes(sk)
        else:
            raise RuntimeError(f"{crypto_sign_keypair} returned {ret}")


def sign(message, sk_bytes):
    with ffi_new_fast('_CRYPTO_BYTES_t') as sig,\
         ffi_new_fast('size_t*') as siglen,\
         ffi.from_buffer(message) as m,\
         ffi.from_buffer(sk_bytes) as sk:
        ret = crypto_sign_signature(sig, siglen, m, len(m), sk)
        if ret == 0:
            assert siglen[0] == len(sig)
            return bytes(sig)
        else:
            raise RuntimeError(f"{crypto_sign_signature} returned {ret}")


def verify(signature, message, pk_bytes):
    with ffi.from_buffer(signature) as sig, # FIXME validate length\
         ffi.from_buffer(message) as m,\
         ffi.from_buffer(pk_bytes) as pk:
        ret = crypto_sign_verify(sig, len(sig), m, len(m), pk)
        if ret == 0:
            return
        else:
            raise ValueError("signature failed to verify.")


def verify_bool(signature, message, pk_bytes):
    with ffi.from_buffer(signature) as sig, # FIXME validate length\
         ffi.from_buffer(message) as m,\
         ffi.from_buffer(pk_bytes) as pk:
        ret = crypto_sign_verify(sig, len(sig), m, len(m), pk)
        return (ret == 0)
