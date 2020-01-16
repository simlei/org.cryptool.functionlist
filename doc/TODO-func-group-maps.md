# Functionality groups

## Naming schemes

**Naming schemes**

- "XYZ" - Anwendung des Verfahrens XYZ
- "XYZ META", XYZ als tragendes Verfahren in META (zB MAC)
- "XYZ Analysis" - Brechen von XYZ als Hauptfunktion

```
a) Aber ich würde Visualisierung und Analyse nicht vereinen.
Man kann es sogar erweitern, dass Cipher und Analysis jeweils mit einem
angehängten "Visual" einen neuen Oberbegriff ergeben. Es gibt also
zusätzlich:

- "XYZ Visual" - Visualsierung von XYZ

==> CT2 [C] Classic Ciphers\ Enigma kann unter 2 Oberbegriffen stehen:
     - Enigma
     - Enigma Visual  (denn es gibt einen Präsentationsmodus dazu)
```
```
b) Protocols and Formats like TLS, PKCS: auch ein extra Oberbegriff.
==> PKCS#1 Attack Visual
```
```
c) Misc

- "AES Brute-Force Attack" in "AES Analysis" umbenennen?
- Typische Abkürzungen sollten beim Oberbegriff dabei sein:
   Ant Colony Optimization  ==>  Ant Colony Optimization (ACO)
   Homomorphic encryption  ==>  Homomorphic encryption (HE)
   Verifiable secret sharing  ==>  Verifiable secret sharing (VSS)
```

## Fragen Naming schemes

**Lattice**
```
++++ Lattice-Based Attacks - Merkle-Hellman
CT2:N \ Crypto tutorials \ Lattice-based cryptography \ Lattice-based cryptanalysis \ Merkle-Hellman Knapsack
++++ Lattice-Based Attacks - RSA
CT2:N \ Crypto tutorials \ Lattice-based cryptography \ Lattice-based cryptanalysis \ RSA (Coppersmith's attack)
++++ Lattice-Based Cryptosystems - GGH
CT2:N \ Crypto tutorials \ Lattice-based cryptography \ Lattice-based cryptography \ GGH
++++ Lattice-Based Cryptosystems - LWE
CT2:N \ Crypto tutorials \ Lattice-based cryptography \ Lattice-based cryptography \ LWE
++++ Lattice-Based Problems - Closest Vector Problem (CVP)
CT2:N \ Crypto tutorials \ Lattice-based cryptography \ Closest Vector Problem (CVP) \ Find closest vector
++++ Lattice-Based Problems - Shortest Vector Problem (SVP) - Gauss
CT2:N \ Crypto tutorials \ Lattice-based cryptography \ Shortest Vector Problem (SVP) \ Gauss algorithm
++++ Lattice-Based Problems - Shortest Vector Problem (SVP) - LLL
CT2:N \ Crypto tutorials \ Lattice-based cryptography \ Shortest Vector Problem (SVP) \ LLL algorithm
```

** Misc **

- Eigennamen + "Cipher" etc, oder ohne suffix?
- SHA-1, -2, T-151(?) v1 v2 etc, SHA 256, CRC-...? oder zusammen fassen (große Cluster...)

- "MD5 Collisions" vs. standard alternatives (Collisions -> "Attack", "Analysis", ...)

- PKCS1 Attack - früher (Kühn), (Bleichenbacher) unterteilt -- so belassen oder unter "PKCS1 Attack"?

- Prime Number -> Prime number
    - Untergruppen (althergebracht)
        - Tutorial (nur der Ober-Menüpunkt "world of primes")
        - Test
        - Distribution

- Gemischte Einordnung: habe es erst mal unter "QR" getan
    - CT2:dynamic:7bf9e18a;QR code;CT2:T \ Codes \ QR Code Encryption
    - CT2:dynamic:bb7249d8;<enter value here>;CT2:T \ Codes \ RSA signed QR code

- Transposition double / single column zusammenfassen?

- bisherige unklare unterscheidung zw. Analyse und Visualisierung:

bisher (in Visualisierung eingeordnet):

```
CT2:en:static:37;Avalanche Visualization;CT2:C;CT2:C\ Tools\ Misc\ Avalanche Visualization;10) Learning Aids and Visualizations
CT2:en:static:38;Avalanche Visualization;CT2:T;CT2:T\ Cryptanalysis\ Modern\ Avalanche (AES);10) Learning Aids and Visualizations
CT2:en:static:39;Avalanche Visualization;CT2:T;CT2:T\ Cryptanalysis\ Modern\ Avalanche (classic ciphers);10) Learning Aids and Visualizations
CT2:en:static:40;Avalanche Visualization;CT2:T;CT2:T\ Cryptanalysis\ Modern\ Avalanche (compare classic ciphers);10) Learning Aids and Visualizations
CT2:en:static:41;Avalanche Visualization;CT2:T;CT2:T\ Cryptanalysis\ Modern\ Avalanche (DES);10) Learning Aids and Visualizations
CT2:en:static:42;Avalanche Visualization;CT2:T;CT2:T\ Cryptanalysis\ Modern\ Avalanche (hash functions);10) Learning Aids and Visualizations
CT2:en:static:43;Avalanche Visualization;CT2:T;CT2:T\ Cryptanalysis\ Modern\ Avalanche (modern ciphers);10) Learning Aids and Visualizations
```
doch besser Analyse?

auch: "Avalanche Effect" stattdessen? (gerade so umgesetzt)

- automatic mode != tutorial?
    - `CT2:dynamic:efd62fe7;Differential cryptanalysis Tutorial;CT2:T \ Cryptanalysis \ Modern \ Differential Cryptanalysis Tutorial 3`
    - `CT2:dynamic:8551f5f9;Differential cryptanalysis;CT2:T \ Cryptanalysis \ Modern \ Differential Cryptanalysis Tutorial 3 (automatic mode)`

- Oberbegriffe "T310 / 50" mit "T310" zusammen?

- Oberbegriffe Paillier vs Paillier Cryptosystem

- Oberbegriffe "Factorization with GNFS" vs "Factorization of a number"

- Gruppierung dieser Algorithmen?
    - `CT2:dynamic:cd7ceca9;<enter value here>later;CT2:C \ Hash functions \ HKDF SHA-256`
    - `CT2:dynamic:79c0e4cc;<enter value here>later;CT2:C \ Hash functions \ KKDF SHA-256`
    - `CT2:dynamic:3cd9e5ac;<enter value here>later;CT2:C \ Hash functions \ KKDF SHAKE256`
