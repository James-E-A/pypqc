# Changelog

## 0.0.6.2 (2024-02-09)

- Added Mac OS support.

## 0.0.6.1 (2024-01-26)

- Upstream security fix for KyberSlash (both versions).
  https://github.com/PQClean/PQClean/commit/3b43bc6fe46fe47be38f87af5019a7f1462ae6dd

## 0.0.6.2 (2024-01-22)

- Added HQC, with parameter sets hqc-128, hqc-192, and hqc-256.

## 0.0.5 (2024-01-15)

- Added Falcon, with parameter sets Falcon-512 and Falcon-1024 (compressed
  version only, pending upstream https://www.github.com/PQClean/PQClean/pull/530.)

## 0.0.4 (2024-01-15)

- Added Kyber, with parameter sets Kyber512, Kyber768, and Kyber1024.

## 0.0.3 (2024-01-15)

- Added Dilithium signatures (detached only) with parameter sets
  Dilithium2, Dilithium3, and Dilithium5. (No AES-based version was
  added.)

## 0.0.2 (2024-01-11)

- Added SPHINCS+ signatures (detached only) with parameter sets
  sha2_128f_simple, sha2_128s_simple, sha2_192f_simple, sha2_192s_simple,
  sha2_256f_simple, sha2_256s_simple, shake_128f_simple, shake_128s_simple,
  shake_192f_simple, shake_192s_simple, shake_256f_simple, and
  shake_256s_simple. (No Haraka version was added; no Robust version was
  added.)

## 0.0.1 (2023-12-21)

- Added McEliece KEM, with parameter sets 348864, 460869, 6688128, and
  6960119 (only "Clean, Fast" implementations; the Plaintext Confirmation
  version was not added; only the NIST Round-4 version was.)
