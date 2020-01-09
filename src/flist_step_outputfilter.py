
def PreprocessCT2(input: Path, output: Path, language: str):
    # read in
    if language == "en":
        pass
        # delete:
        # 1a)
        # SIGABA Known Plaintext;C;
        # ;[C];Tools\ Misc\ SIGABA Known Plaintext
        # 1b)
        # Ciphertext-only;W;
        # [...]
        # ;[W];Cryptanalysis\ Modern Encryption\ Symmetric Encryption\ DES\ Ciphertext-only
    elif language == "de":
        # delete:
        pass
        # 2a)
        # Ciphertext-only-Analyse;W;
        # ;[W];Kryptoanalyse\ Moderne Verschlüsselung\ Symmetrische Verschlüsselung\ DES\ Ciphertext-only-Analyse
    # write out
    return
