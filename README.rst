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
      enter the appropriate environment before you get started. (For AMD64,
      this will be "x64 Native Tools Command Prompt for VS 2022"; for 32-bit
      x86, this will be "Developer Command Prompt for VS 2022"; for other
      situations, see `the documentation <https://learn.microsoft.com/en-us/cpp/build/building-on-the-command-line?view=msvc-170>`_.)

  - If you're on Mac,
    `reportedly Homebrew is a good choice <https://cffi.readthedocs.io/en/latest/installation.html#macos-x>`_.

    - It looks like you will also need `pkg-config <https://freedesktop.org/wiki/Software/pkg-config/>`_
      and `libffi <https://sourceware.org/libffi/>`_, ideally installed via Homebrew,
      to build this.

      .. OH MY GODDDDDD WHY IS RST FORMATTING SO HARD https://stackoverflow.com/posts/comments/65215146

    - If anyone wants to contribute better documentation here, or donate
      hardware so I can write better documentation (as well as creating
      some less SaaS-based CI), that'd be appreciated.

  - If you're on Linux, install build-essential_ or `"Development Tools"`_ or
    something like that.

  - (I haven't tested it, but if you're allergic to installing things outside
    the venv you might be able to use
    `this C compiler <https://pypi.org/project/ziglang/>`_...)

Getting started:
----------------

0. Make sure you've got Git and Python and access to the C compiler, however you need to do that.

1. (Development branch) run

   .. code-block:: cmd

      git clone "https://github.com/James-E-A/pypqc" -b "rewrite/2024-08-23" "pypqc-rewrite-2024-08-23" && cd "pypqc-rewrite-2024-08-23"

2. Run ``python -m pip install build`` (or whatever your favorite PEP 517 compatible build tool is)

   - Before you do this, you could also consider `creating a venv <https://www.bitecode.dev/p/relieving-your-python-packaging-pain>`_

     - for Windows:

       .. code-block:: cmd

          py -m venv .venv --prompt . && .venv\Scripts\activate.bat

     - for Linux and Mac:

       .. code-block:: bash

           # https://packages.ubuntu.com/jammy/python/python3-venv
           python3 -m venv .venv --prompt . && . .venv/bin/activate

3. Run

   .. code-block:: cmd

      python -m build -o dist projects/pypqc-cffi-bindings-libre

   to compile the baseline suite, which includes 1 KEM and 2 signature
   algorithms. This will produce a wheel file in ``dist``, which you can
   then install.

   - Editable / "develop" mode not supported currently (CFFI will have to
     `support this <https://setuptools.pypa.io/en/latest/userguide/extension.html#setuptools.command.build.SubCommand.editable_mode>`_
     before it's even on the table.)

   - If you get error 1104 when trying to compile on Windows, make a folder ``C:\temp``, then try ``set "TMPDIR=C:\temp"`` and try again. (https://discuss.python.org/t/-/44077/5)

4. Repeat step 3 for each set of bindings you want to compile.

5. Once the bindings have been installed, you can do the same for the
   ``pypqc`` package itself, which wraps the bindings in usable Python
   functions.

6. If you made any serious changes to the codebase, run ``python scripts/make.py``
   to regenerate the files under ``projects/*bindings*/{cffi_modules,src/pqc/_lib}``
   to reflect your changes, before going back to step 3.


.. _`McEliece Signatures`: https://web.archive.org/web/20190501070335/https://link.springer.com/content/pdf/10.1007/3-540-45682-1_10.pdf#%5B%7B%22num%22%3A43%2C%22gen%22%3A0%7D%2C%7B%22name%22%3A%22Fit%22%7D%5D
.. _`Hybrid Encryption`: https://en.wikipedia.org/wiki/Hybrid_encryption
.. _`KEM-TRANS`: https://www.ietf.org/archive/id/draft-perret-prat-lamps-cms-pq-kem-00.html#name-kem-key-transport-mechanism
.. _`message encapsulation`: https://en.wikipedia.org/wiki/Cryptographic_Message_Syntax

.. _cffi: https://cffi.readthedocs.io/en/release-1.16/
.. _wheel: https://wheel.readthedocs.io/
.. _setuptools: https://setuptools.pypa.io/en/stable/
.. _`Python Headers`: https://packages.ubuntu.com/jammy/python3-dev
.. _build-essential: https://packages.ubuntu.com/jammy/build-essential
.. _`"Development Tools"`: https://git.rockylinux.org/rocky/comps/-/blob/e6c8f29a7686326a731ea72b6caa06dabc7801b5/comps-rocky-9-lh.xml#L2169
