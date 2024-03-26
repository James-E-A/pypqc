# Security Policy

## Supported Versions

* 0.7.X

## Reporting a Vulnerability

### Vulnerabilities in the implementations

First, check to see if our upstream, PQClean, has issued any updates, and open a
ticket with them if necessary according to their policy:
https://github.com/PQClean/PQClean/security/policy

If they claim no patch is available, you may have to escalate to the creators/implementors:

* Classic McEliece: https://classic.mceliece.org/nist/mceliece-submission-20221023.pdf#:~:text=E%2Dmail%20address,%2Eyp%2Eto

* Kyber: https://github.com/pq-crystals/kyber/issues?q=security

* HQC: https://pqc-hqc.org/contact.html

* SPHINCS+: https://github.com/sphincs/sphincsplus/issues?q=security

* Dilithium: https://github.com/pq-crystals/dilithium/issues?q=security

* Falcon: https://falcon-sign.info/falcon.pdf#:~:text=Zhang-,falcon,ens%2Efr

If upstream has already issued an update, but we have not included it,
please open a ticket on our issue tracker about that.

If you want this process to occur faster, contributions are currently being sought
via [ticket #19](https://github.com/JamesTheAwesomeDude/pypqc/issues/19) on our
issue tracker.

### Security flaws in the actual algorithms

First, check to see if the flaw has already been publicly disclosed:
https://csrc.nist.gov/Projects/post-quantum-cryptography/email-list

If the flaw has already been reported on, please proceed with the "Vulnerabilities
in the implementations" process above.

If the flaw has **not** been reported on yet:

- For algorithms which have **not** been standardized yet, please publish your
findings on that mailing list.

- For algorithms which **have** been standardized already (see the NIST page on
[Post-Quantum Cryptography Standardization](https://csrc.nist.gov/Projects/post-quantum-cryptography/Post-Quantum-Cryptography-Standardization)
for the current list), please contact the algorithm's creators/implementors directly
as soon as possible.

### Vulnerabilities in the bindings

If the vulnerability is *not* with the implementation, or with the actual algorithms,
but with our Python bindings, please open a ticket on our issue tracker about that.

## Reporting a Supply-Chain Compromise

If you suspect some element of the supply chain has been compromised
(e.g. pypqc has merged fake commits, or the PyPI project page has been
compromised, etc.), please e-mail james{{dot}}edington{{?}}uah.edu ASAP.
