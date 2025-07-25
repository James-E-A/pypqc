#
#  Part of the PyPQC bindings project
#
#  Originally written by: James Edington Administator
#
#  SPDX-License-Identifier: MIT OR Apache-2.0
#

from pqc._lib.kem_hqc.libhqc_128_clean import ffi, lib

ffi_new_fast = ffi.new_allocator(should_clear_after_alloc=False)
crypto_kem_keypair = lib.crypto_kem_keypair
crypto_kem_enc = lib.crypto_kem_enc
crypto_kem_dec = lib.crypto_kem_dec

__all__ = ["keypair", "encap", "decap"]


def keypair():
    with ffi_new_fast('_CRYPTO_PUBLICKEY_t') as pk,\
         ffi_new_fast('_CRYPTO_SECRETKEY_t') as sk:
        ret = crypto_kem_keypair(pk, sk)
        if ret == 0:
            return bytes(pk), bytes(sk)
        else:
            raise RuntimeError(f"{crypto_kem_keypair} returned {ret}")


def encap(pk_bytes):
    with ffi_new_fast('_CRYPTO_CIPHERTEXT_t') as c,\
         ffi_new_fast('_CRYPTO_PLAINTEXT_t') as key,\
         ffi.from_buffer(pk_bytes) as pk: # FIXME validate length
        ret = crypto_kem_enc(c, key, pk)
        if ret == 0:
            return bytes(c), bytes(key)
        else:
            raise RuntimeError(f"{crypto_kem_enc} returned {ret}")


def decap(ct_bytes, sk_bytes):
    with ffi_new_fast('_CRYPTO_PLAINTEXT_t') as key,\
         ffi.from_buffer(ct_bytes) as c,\
         ffi.from_buffer(sk_bytes) as sk: # FIXME validate length
        ret = crypto_kem_dec(key, c, sk)
        if ret == 0:
            return bytes(key)
        else:
            raise RuntimeError(f"{crypto_kem_dec} returned {ret}")

