Usage
=====

Simply install from PyPI with ``pip install pypqc``, or see "Development" below
if you want to tinker on the codebase!

KEMs
----

McEliece, Kyber, and HQC are currently provided, all with the same interface.::

    # Available: hqc_128, hqc_192, hqc_256,
    # kyber512, kyber768, kyber1024,
    # mceliece348864, mceliece460896,
    # mceliece6688128, mceliece6960119, mceliece8192128
    from pqc.kem import mceliece6960119 as kemalg
    
    
    # 1. Keypair generation
    pk, sk = kemalg.keypair()
    
    
    # 2. Key encapsulation
    ss, kem_ct = kemalg.encap(pk)
    
    
    # 3. Key de-encapsulation
    ss_result = kemalg.decap(kem_ct, sk)
    assert ss_result == ss

Capabilities *not* included in PQClean, such as `McEliece signatures`_,
`Hybrid Encryption`_ or `KEM-TRANS`_, and `message encapsulation`_, are
*not* going to be implemented in this library. (Exception: `Plaintext
Confirmation <https://www.github.com/thomwiggers/mceliece-clean/issues/3>`_
is on the agenda for inclusion even if upstream ultimately decides to exclude
it.)

Signature Algorithms
--------------------

SPHINCS+, Dilithium, and Falcon are provided, all with the same interface.::

    # Supported: dilithium2, dilithium3, dilithium5,
    # falcon_512, falcon_512_padded, falcon_1024, falcon_1024_padded,
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
``verify()`` each others' signatures. The CT version is not currently planned.

Development
===========

Dependencies:
-------------

- Python 3 (tested mainly on CPython 3.9, 3.10, 3.11, and 3.12; and on PyPy
  7.3.12)

- cffi_

  - Transitive non-PyPI build-time dependency: `Python Headers`_ (only Linux users
    need to manually install these; they come OOtB on Windows. Not sure about Mac.)

- setuptools_ (build-time dependency)

- wheel_ (build-time dependency)

- a C compiler (build-time dependency)

  - If you're on Windows, https://visualstudio.microsoft.com/visual-cpp-build-tools/

    - If setuptools is having trouble finding your compiler, make sure to
      first enter the appropriate environment. (For AMD64, this will be
      "x64 Native Tools Command Prompt for VS 2022"; for 32-bit x86, this
      will be "Developer Command Prompt for VS 2022"; for other situations,
      see `the documentation <https://learn.microsoft.com/en-us/cpp/build/building-on-the-command-line?view=msvc-170>`_.)

  - If you're on Mac,
    `reportedly Homebrew is a good choice <https://cffi.readthedocs.io/en/latest/installation.html#macos-x>`_.

    - It looks like you will also need ``pkgconfig`` and ``libffi``, ideally
      installed via Homebrew, to build this.

  - If you're on Linux, install build-essential_ or `'Development Tools'`_ or
    something like that.

  - (I haven't tested it, but if you're allergic to installing things outside
    the venv you might be able to use
    `this C compiler <https://pypi.org/project/ziglang/>`_...)

Getting started:
----------------

0. Maybe `use a venv <https://www.bitecode.dev/p/relieving-your-python-packaging-pain>`_
   or whatever if you want to

   - for Windows: ``py -m venv .venv & .venv\Scripts\activate.bat``

   - for Linux and Mac: ``python3 -m venv .venv; . .venv/bin/activate``
     (first `install it <https://packages.ubuntu.com/jammy/python/python3-venv>`_,
     if needed)

1. Run ``python -m pip install .``

   - Alternatively: you may get cleaner building with ``python -m build .``
     (only after ``python -m pip install build``)

   - Editable / "develop" mode not supported currently (CFFI will have to
     `support this <https://setuptools.pypa.io/en/latest/userguide/extension.html#setuptools.command.build.SubCommand.editable_mode>`_
     before it's even on the table.)

     - If you get error 1104 when trying to compile, make a folder ``C:\temp``, then try ``set "TMPDIR=C:\temp"`` and try again. (https://discuss.python.org/t/-/44077/5)

2. Run ``python -m pqc.demo`` to test it. If it prints "OK" and exits, the
   functions are almost certainly not broken. (Ideally, run this from a
   DIFFERENT directory, such as your home folder, so you can be sure it's
   being imported properly and not being masked by the local copy.)

   - N.B. / FIXME: this function is currently NOT a full test suite;
     it only does a single encap-decap cycle with
     the default implementation of mceliece6960119.
     It does NOT test any other version of McEliece,
     or any signature algorithm.


.. _cffi: https://cffi.readthedocs.io/en/release-1.16/
.. _wheel: https://wheel.readthedocs.io/
.. _setuptools: https://setuptools.pypa.io/en/stable/
.. _`Python Headers`: https://packages.ubuntu.com/jammy/python3-dev
.. _build-essential: https://packages.ubuntu.com/jammy/build-essential
.. _`'Development Tools'`: https://git.rockylinux.org/rocky/comps/-/blob/e6c8f29a7686326a731ea72b6caa06dabc7801b5/comps-rocky-9-lh.xml#L2169

.. _`McEliece Signatures`: https://inria.hal.science/inria-00072511
.. _`Hybrid Encryption`: https://en.wikipedia.org/wiki/Hybrid_encryption
.. _`KEM-TRANS`: https://www.ietf.org/staging/draft-prat-perret-lamps-cms-pq-kem-00.html
.. _`message encapsulation`: https://en.wikipedia.org/wiki/Cryptographic_Message_Syntax
