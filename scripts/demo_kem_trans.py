from Crypto.Cipher import AES # https://pypi.org/project/pycryptodome/
from Crypto.Hash import SHAKE256

from types import SimpleNamespace


def siv_encrypt(k, m, *, aad=None):
    # https://datatracker.ietf.org/doc/html/rfc5297#section-2.6
    cipher = AES.new(k, AES.MODE_SIV)
    if aad is not None:
        cipher.update(aad)
    ct, iv = cipher.encrypt_and_digest(m)
    assert len(iv) == AES.block_size # SIV uses cipher's native block size, regardless of key size
    return iv + ct


def siv_decrypt(k, ct_siv, *, aad=None):
    # https://datatracker.ietf.org/doc/html/rfc5297#section-2.7
    iv, ct = ct_siv[:AES.block_size], ct_siv[AES.block_size:]
    cipher = AES.new(k, AES.MODE_SIV)
    if aad is not None:
        cipher.update(aad)
    return cipher.decrypt_and_verify(ct, iv)


aes_siv = SimpleNamespace(encrypt=siv_encrypt, decrypt=siv_decrypt)


def shake256_256(m):
    h = SHAKE256.new()
    h.update(m)
    return h.read(32)


def kem_trans(kemalg, k, pk, *, wrapalg=aes_siv, kdf=shake256_256):
    # https://www.ietf.org/archive/id/draft-perret-prat-lamps-cms-pq-kem-00.html#name-senders-operations
    ct, ss = kemalg.encap(pk)
    kek = kdf(ss)
    wk = wrapalg.encrypt(kek, k)
    ek = wk + ct
    return ek


def kem_trans_unwrap(kemalg, ek, sk, *, wrapalg=aes_siv, kdf=shake256_256):
    # https://www.ietf.org/archive/id/draft-perret-prat-lamps-cms-pq-kem-00.html#name-recipients-operations
    wk, ct = ek[:-kemalg._lib.CRYPTO_CIPHERTEXTBYTES], ek[-kemalg._lib.CRYPTO_CIPHERTEXTBYTES:]
    try:
        ss = kemalg.decap(ct, sk)
    except TypeError as e: raise
    except Exception as e: raise ValueError("decryption error") from None
    kek = kdf(ss)
    try:
        k = wrapalg.decrypt(kek, wk)
    except TypeError as e: raise
    except Exception as e: raise ValueError("decryption error") from None
    return k


if __name__ == '__main__':
    # DEMO
    from pqc.kem import mceliece6960119f as kemalg # https://pypi.org/project/pypqc/
    from os import urandom
    k = urandom(69) # kem-trans supports wrapping arbitrary data blobs
    pk, sk = kemalg.keypair()
    ek = kem_trans(kemalg, k, pk)
    k_result = kem_trans_unwrap(kemalg, ek, sk)
    if k == k_result:
        print("OK")
    else:
        raise ValueError("decryption error") # this should seriously NEVER occur
