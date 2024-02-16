# Security Policy

## Supported Versions

* `0.6.X`

## Reporting a Vulnerability

### Vulnerabilities in the actual algorithms

First, check to see if upstream has issued any updates, and open a
ticket with them if necessary according to their policy:
https://github.com/PQClean/PQClean/security/policy

If they claim no patch is available, you may have to escalate:

* Classic McEliece: https://classic.mceliece.org/nist/mceliece-submission-20221023.pdf#:~:text=E%2Dmail%20address,%2Eyp%2Eto

* Kyber: https://github.com/pq-crystals/kyber/issues?q=security

* HQC: https://pqc-hqc.org/contact.html

* SPHINCS+: https://github.com/sphincs/sphincsplus/issues?q=security

* Dilithium: https://github.com/pq-crystals/dilithium/issues?q=security

* Falcon: https://falcon-sign.info/falcon.pdf#:~:text=Zhang-,falcon,ens%2Efr

If upstream has already issued an update, but we have not included it,
please open a ticket on the issue tracker about that.

### Vulnerabilities in the bindings

If the vulnerability is *not* with the actual algorithms, but with our
Python bindings, please open a ticket on the issue tracker about that.

## Reporting a Supply-Chain Compromise

If you believe some element of the supply chain has been compromised
(e.g. pypqc has merged fake commits, or the PyPI project page has been
compromised, etc.), please e-mail james<dot>edington<?>uah.edu ASAP.
