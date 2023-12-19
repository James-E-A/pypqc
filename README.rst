Usage
=====

::

    from pqc.kem import mceliece6960119
    
    
    # 1. Keypair generation
    pk, sk = mceliece6960119.kem_keypair()
    
    # WARNING these^ are some heavy keys
    # (1MiB public, 13.6KiB private)
    # if you must display them, consider base64.encode(...)
    
    
    # 2. Key encapsulation
    ss, kem_ct = mceliece6960119.kem_enc(pk)
    
    # 2(a). Hybrid KEM-Wrap
    cek = urandom(32)
    symm_ct = MY_SYMMETRIC_CRYPTOSYSTEM.enc(message_plaintext, key=cek)
    kek = MY_KDF(ss, target=MY_KEYWRAP)
    wk = MY_KEYWRAP.enc(cek, key=kek)
    SEND_MESSAGE([kem_ct, wk, symm_ct])
    
    
    # 3. Key de-encapsulation
    ss_result = mceliece6960119.kem_dec(kem_ct, sk)
    assert ss_result == ss
    
    # 3(a) Hybrid KEM Unwrap
    kek = MY_KDF(ss_result, target=MY_KEYWRAP)
    cek = MY_KEYWRAP.dec(wk, key=kek)
    message_result = MY_SYMMETRIC_CRYPTOSYSTEM.dec(symm_ct, key=cek)

Currently, only the McEliece KEM is exposed. Kyber and HQC are planned
next; after them will be the signature algorithms.

Capabilities *not* included in PQClean, such as `McEliece signatures`_,
`Hybrid Encryption`_ (depicted above), and `message encapsulation`_, are
*not* going to be implemented in this library. (Exception: `Plaintext
Confirmation <https://www.github.com/thomwiggers/mceliece-clean/issues/3>`_
is on the agenda for inclusion even if upstream ultimately decides to exclude
it.)


Development
===========

Dependencies:

- Python 3 (tested mainly on CPython 3.10, 3.11, and 3.12; and on PyPy 7.3.12)

  - TBD: fix an oldest supported Python version / test on versions older than 3.10

- cffi_ (from PyPI; build-time dependency only)

  - Linux users may not have got the `Python Headers`_ included with their Python installation; cffi requires them

- setuptools_ (from PyPI; build-time dependency only)
- a C compiler (build-time dependency only)

  - If you're on Windows, https://visualstudio.microsoft.com/visual-cpp-build-tools/ AND THEN make sure you enter the appropriate environment (for AMD64, "x64 Native Tools Command Prompt for VS 2022"; for 32-bit x86, "Developer Command Prompt for VS 2022"; for other situations, see `the documentation <https://learn.microsoft.com/en-us/cpp/build/building-on-the-command-line?view=msvc-170>`_.)
  - If you're on Linux, install build-essential_ or `group "Development Tools"`_ or something like that

  - haven't tested it, but if you're allergic to installing things outside the venv you might be able to use `this C compiler <https://pypi.org/project/ziglang/>`_

Getting started:

0. Maybe `use a venv <https://www.bitecode.dev/p/relieving-your-python-packaging-pain>`_ or whatever if you want to

   - for Linux: ``python3 -m venv .venv; . .venv/bin/activate`` (`install it <https://packages.ubuntu.com/jammy/python/python3-venv>`_ if needed)
   - for Windows: ``py -m venv .venv & .venv\Scripts\activate.bat``

1. Run ``python -m pip install -r requirements-dev.txt``

2. Run ``python -m pip install .``

   - editable not supported currently (CFFI will have to `support this <https://setuptools.pypa.io/en/latest/userguide/extension.html#setuptools.command.build.SubCommand.editable_mode>`_ before it's even on the table)

   - Alternatively: cleaner building with ``python -m build .`` (only after ``python -m pip install build``)

3. Run ``python -m pqc.demo`` to test it. If it prints "OK" and exits, the functions are almost certainly not broken. (Ideally, run this from a DIFFERENT directory, such as your home folder, so you can be sure it's being imported properly)


.. _cffi: https://cffi.readthedocs.io/en/release-1.16/
.. _setuptools: https://setuptools.pypa.io/en/stable/
.. _`Python Headers`: https://packages.ubuntu.com/jammy/python3-dev
.. _build-essential: https://packages.ubuntu.com/jammy/build-essential
.. _`group "Development Tools"`: https://git.rockylinux.org/rocky/comps/-/blob/e6c8f29a7686326a731ea72b6caa06dabc7801b5/comps-rocky-9-lh.xml#L2169

.. _`McEliece Signatures`: https://inria.hal.science/inria-00072511
.. _`Hybrid Encryption`: https://en.wikipedia.org/wiki/Hybrid_encryption
.. _`message encapsulation`: https://en.wikipedia.org/wiki/Cryptographic_Message_Syntax
