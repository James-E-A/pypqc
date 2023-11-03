Development
===========

Dependencies:

- Python 3 (tested mainly on 3.10, 3.11, and 3.12)
- asn1_ (from PyPI)
- cryptography_ (from PyPI)
- cffi_ (from PyPI; build-time dependency only)
- a C compiler (build-time dependency only)

  - If you're on Windows, https://visualstudio.microsoft.com/visual-cpp-build-tools/ AND THEN make sure you launch "Developer Command Prompt for VS 2022" or whatever
  - If you're on Linux, install build-essential_ or `"Development Tools"`_ or something like that

    - Linux users may also not have got the `Python Headers`_ free with their xbox and will have to go beg on the streets to get them before cffi will work

Getting started:

0. Maybe [use a venv](https://www.bitecode.dev/p/relieving-your-python-packaging-pain) or whatever if you
1. Run ``cffi_compile.py``
2. Run ``main.py`` and check out the ``demo_*`` functions

.. _cffi: https://cffi.readthedocs.io/en/release-1.16/
.. _asn1: https://github.com/andrivet/python-asn1
.. _cryptography: https://github.com/pyca/cryptography
.. _`Python Headers`: https://packages.ubuntu.com/jammy/python3-dev
.. _build-essential: https://packages.ubuntu.com/jammy/build-essential
.. _`"Development Tools"`: https://git.rockylinux.org/rocky/comps/-/blob/e6c8f29a7686326a731ea72b6caa06dabc7801b5/comps-rocky-9-lh.xml#L1768

Usage
=====

(TODO, not user-facing at this time)
