Installation
============

(Installation instructions TODO. For now, install the “build-time”
dependencies and it should work. Package does not have run-time dependency
on any 3rd-party modules.)


Usage
=====


KEMs
----

(Currently, only the McEliece KEM is exposed. Kyber and HQC are TODO.)::

    from pqc.kem import mceliece6960119
    
    
    # 1. Keypair generation
    pk, sk = mceliece6960119.kem_keypair()
    
    # WARNING these^ are some heavy keys
    # (1MiB public, 13.6KiB private)
    # if you must display them, consider base64.encode(...)
    
    
    # 2. Key encapsulation
    ss, kem_ct = mceliece6960119.kem_enc(pk)
    
    # 2(a). Hybrid KEM-Wrap
    #cek = urandom(32)
    #symm_ct = MY_SYMMETRIC_CRYPTOSYSTEM.enc(message_plaintext, key=cek)
    #kek = MY_KDF(ss, target=MY_KEYWRAP)
    #wk = MY_KEYWRAP.enc(cek, key=kek)
    #SEND_MESSAGE([kem_ct, wk, symm_ct])
    
    
    # 3. Key de-encapsulation
    ss_result = mceliece6960119.kem_dec(kem_ct, sk)
    assert ss_result == ss
    
    # 3(a) Hybrid KEM Unwrap
    #kek = MY_KDF(ss_result, target=MY_KEYWRAP)
    #cek = MY_KEYWRAP.dec(wk, key=kek)
    #message_result = MY_SYMMETRIC_CRYPTOSYSTEM.dec(symm_ct, key=cek)

Capabilities *not* included in PQClean, such as `McEliece signatures`_,
`Hybrid Encryption`_ (depicted above), and `message encapsulation`_, are
*not* going to be implemented in this library. (Exception: `Plaintext
Confirmation <https://www.github.com/thomwiggers/mceliece-clean/issues/3>`_
is on the agenda for inclusion even if upstream ultimately decides to exclude
it.)

Signature Algorithms
--------------------

(TODO)


Development
===========

Dependencies:
-------------

- Python 3 (tested mainly on CPython 3.9, 3.10, 3.11, and 3.12; and on PyPy
  7.3.12)

- cffi_ (from PyPI; build-time dependency only)

  - Transitive dependency: `Python Headers`_ (I think these come OOTB on
    Windows)

- setuptools_ (from PyPI; build-time dependency only)

- a C compiler (build-time dependency only)

  - If you're on Windows, https://visualstudio.microsoft.com/visual-cpp-build-tools/

    - If setuptools is having trouble finding your compiler, make sure to
      first enter the appropriate environment. (For AMD64, this will be
      "x64 Native Tools Command Prompt for VS 2022"; for 32-bit x86, this
      will be "Developer Command Prompt for VS 2022"; for other situations,
      see `the documentation <https://learn.microsoft.com/en-us/cpp/build/building-on-the-command-line?view=msvc-170>`_.)

  - If you're on Mac,
    `reportedly Homebrew + pkg-config + libffi is a good choice <https://cffi.readthedocs.io/en/latest/installation.html#macos-x>`_.

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

2. Run ``python -m pqc.demo`` to test it. If it prints "OK" and exits, the
   functions are almost certainly not broken. (Ideally, run this from a
   DIFFERENT directory, such as your home folder, so you can be sure it's
   being imported properly and not being masked by the local copy.)


.. _cffi: https://cffi.readthedocs.io/en/release-1.16/
.. _setuptools: https://setuptools.pypa.io/en/stable/
.. _`Python Headers`: https://packages.ubuntu.com/jammy/python3-dev
.. _build-essential: https://packages.ubuntu.com/jammy/build-essential
.. _`'Development Tools'`: https://git.rockylinux.org/rocky/comps/-/blob/e6c8f29a7686326a731ea72b6caa06dabc7801b5/comps-rocky-9-lh.xml#L2169

.. _`McEliece Signatures`: https://inria.hal.science/inria-00072511
.. _`Hybrid Encryption`: https://en.wikipedia.org/wiki/Hybrid_encryption
.. _`message encapsulation`: https://en.wikipedia.org/wiki/Cryptographic_Message_Syntax


Copyright
=========

**Except as noted below**, all files original or contributed works,
Copyright (c) 2023 James Edington Administrator.

**Except as noted below**, all files provided under the terms of
`LICENSE <LICENSE.txt>`_ in this folder.

Exceptions:
-----------

* ``Lib/PQClean/common/aes.*``: Provided under The MIT License; Copyright (c) 2016 Thomas Pornin.

* ``Lib/PQClean/common/fips202.*``: Public domain; from Ronny Van Keer, Gilles Van Assche, Daniel J. Bernstein, and Peter Schwabe.

* ``Lib/PQClean/common/keccak4x``: Public domain (CC0); from Gilles Van Assche and Ronny Van Keer.

* ``Lib/PQClean/common/nistseedexpander.*``: ⚠️ **Ambiguously licensed!** Copyright (c) 2017 Lawrence E. Bassham, with contributions from Sebastian Verschoor.

* ``Lib/PQClean/common/randombytes.*``: Provided under The MIT License; Copyright (c) 2017 Daan Sprenkels.

* ``Lib/PQClean/common/sha2.*``: Public domain.

* ``Lib/PQClean/common/sp800-185.*``: Public domain (CC0); from Ko Stoffelen.

* ``Lib/PQClean/crypto_kem/hqc-rmrs*``: Public domain.

* ``Lib/PQClean/crypto_kem/kyber*``: Public domain (CC0).

* ``Lib/PQClean/crypto_kem/mceliece*``: Public domain.

* ``Lib/PQClean/crypto_sign/dilithium*``: Public domain.

* ``Lib/PQClean/crypto_sign/falcon*``: ⚠️ **May be patent-encumbered in the United States!** Provided under The MIT License; Copyright (c) 2017-2019 Falcon Project.

* ``Lib/PQClean/crypto_sign/sphincs*``: Public domain (CC0).

* All other files under ``Lib/PQClean``: Public domain (CC0).
