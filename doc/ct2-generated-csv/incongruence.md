# Appears only in english CSV:

1a)
SIGABA Known Plaintext;C;
;[C];Tools\ Misc\ SIGABA Known Plaintext

1b)
Ciphertext-only;W;
[...]
;[W];Cryptanalysis\ Modern Encryption\ Symmetric Encryption\ DES\ Ciphertext-only

# Appears only in german CSV:

2a)
Ciphertext-only-Analyse;W;
;[W];Kryptoanalyse\ Moderne Verschlüsselung\ Symmetrische Verschlüsselung\ DES\ Ciphertext-only-Analyse

# Solution: preliminary

after deleting 1a,2a entirely, and in the case of 1b), only the line after `[...]`, the csv files are congruent. This is done via an initial csv filtering step implemented in org.cryptool.functionlist to not require introducing special cases into CT2 code just now.

In the nighlty build, 1a does not appear. It must be ignored there.
