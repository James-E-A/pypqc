Usage
=====

**Development version. You need a C compiler first.**

Simply install from PyPI with

.. code-block:: cmd

    pip install --pre "pypqc[falcon,hqc,kyber]"

or see "Development" below if you want to tinker on the codebase!

(If you are a stickler for `libre <https://www.gnu.org/philosophy/free-sw.en.html#clarifying>`_
software, you can *leave off* the bracketed bit in the above command to install
only the subset of libraries available under OSI-approved licenses.)

KEMs
----

McEliece, Kyber, and HQC are currently provided, all with the same easy-to-use interface:

.. code-block:: python

    # Available: hqc_128, hqc_192, hqc_256,
    # kyber512, kyber768, kyber1024,
    # mceliece348864, mceliece460896,
    # mceliece6688128, mceliece6960119, mceliece8192128
    from pqc.kem import mceliece6960119 as kemalg
    
    # 1. Keypair generation
    pk, sk = kemalg.keypair()
    
    # 2. Key encapsulation
    kem_ct, ss = kemalg.encap(pk)
    
    # 3. Key de-encapsulation
    ss_result = kemalg.decap(kem_ct, sk)
    assert ss_result == ss

Capabilities *not* included in PQClean, such as `McEliece signatures`_,
`Hybrid Encryption`_ (`KEM-TRANS`_), and `message encapsulation`_, are
*not* going to be implemented in this library as they're all either
higher-level constructions that could be implemented using this library,
or are lower-level constructions that would require a serious cryptographic
implementation effort.

\*Exception: `McEliece w/ Plaintext Confirmation <https://www.github.com/thomwiggers/mceliece-clean/issues/3>`_
is on the agenda for inclusion even if upstream ultimately decides to exclude it.

Signature Algorithms
--------------------

SPHINCS+, Dilithium, and Falcon are provided, all with the same easy-to-use interface:

.. code-block:: python

    # Available: dilithium2, dilithium3, dilithium5,
    # falcon_512, falcon_padded_512, falcon_1024, falcon_padded_1024,
    # sphincs_sha2_128f_simple, sphincs_sha2_128s_simple,
    # sphincs_shake_128f_simple, sphincs_shake_128s_simple,
    # sphincs_sha2_192f_simple, sphincs_sha2_192s_simple,
    # sphincs_shake_192f_simple, sphincs_shake_192s_simple,
    # sphincs_sha2_256f_simple, sphincs_sha2_256s_simple,
    # sphincs_shake_256f_simple, sphincs_shake_256s_simple
    from pqc.sign import sphincs_shake_256s_simple as sigalg
    
    # 1. Keypair generation
    pk, sk = sigalg.keypair()
    
    # 2. Signing
    # (detached signature)
    sig = sigalg.sign(MY_MESSAGE, sk)
    
    # 3. Signature verification
    # (Returns None on success; raises ValueError on failure.)
    sigalg.verify(sig, MY_MESSAGE, pk)

Regarding SPHINCS+: the Simple version is included; the Robust version is is not;
SHA256 and SHAKE256 are included; Haraka is not. See https://github.com/PQClean/PQClean/discussions/548#discussioncomment-8565116
for more information.

Regarding Falcon: the Compressed and Padded versions are included, and are able to
``verify()`` each others' signatures. The CT version is not currently planned for
support in any capacity, even verification.

Development
===========

This package is developed as part of a Monorepo.

See https://github.com/James-E-A/pypqc/tree/rewrite/2024-08-23 for development instructions and details.


.. _`McEliece Signatures`: https://inria.hal.science/inria-00072511
.. _`Hybrid Encryption`: https://en.wikipedia.org/wiki/Hybrid_encryption
.. _`KEM-TRANS`: https://www.ietf.org/archive/id/draft-perret-prat-lamps-cms-pq-kem-00.html#name-kem-key-transport-mechanism
.. _`message encapsulation`: https://en.wikipedia.org/wiki/Cryptographic_Message_Syntax
