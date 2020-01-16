# Misc

# Functionality groups

## Doc

**Naming schemes**

- "XYZ" - Anwendung des Verfahrens XYZ
- "XYZ META", XYZ als tragendes Verfahren in META (zB MAC)
- "XYZ Analysis" - Brechen von XYZ als Hauptfunktion

a) Aber ich würde Visualisierung und Analyse nicht vereinen.
Man kann es sogar erweitern, dass Cipher und Analysis jeweils mit einem
angehängten "Visual" einen neuen Oberbegriff ergeben. Es gibt also
zusätzlich:

- "XYZ Visual" - Visualsierung von XYZ

==> CT2 [C] Classic Ciphers\ Enigma kann unter 2 Oberbegriffen stehen:
     - Enigma
     - Enigma Visual  (denn es gibt einen Präsentationsmodus dazu)


b) Protocols and Formats like TLS, PKCS: auch ein extra Oberbegriff.
==> PKCS#1 Attack Visual

c) Misc

- "AES Brute-Force Attack" in "AES Analysis" umbenennen?
- Typische Abkürzungen sollten beim Oberbegriff dabei sein:
   Ant Colony Optimization  ==>  Ant Colony Optimization (ACO)
   Homomorphic encryption  ==>  Homomorphic encryption (HE)
   Verifiable secret sharing  ==>  Verifiable secret sharing (VSS)

#### Fragen

**Lattice**

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


** Misc **

- Eigennamen + "Cipher" etc, oder ohne suffix?
- SHA-1, -2, T-151(?) v1 v2 etc, SHA 256, CRC-...? oder zusammen fassen (große Cluster...)

- "MD5 Collisions" vs. standard alternatives (attack, analysis, ...)

- "Applications" --> 
    - Watermark creator?

- PKCS1 Attack - früher (Kühn), (Bleichenbacher) unterteilt

- Prime Number -> Prime number
    Tutorial (nur der Ober-Menüpunkt "world of primes")
    Test
    Distribution

- Gemischte Einordnung: habe es erst mal unter "QR" getan
CT2:dynamic:7bf9e18a;QR code;CT2:T \ Codes \ QR Code Encryption
CT2:dynamic:bb7249d8;<enter value here>;CT2:T \ Codes \ RSA signed QR code

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
CT2:dynamic:efd62fe7;Differential cryptanalysis Tutorial;CT2:T \ Cryptanalysis \ Modern \ Differential Cryptanalysis Tutorial 3
CT2:dynamic:8551f5f9;Differential cryptanalysis;CT2:T \ Cryptanalysis \ Modern \ Differential Cryptanalysis Tutorial 3 (automatic mode)

- Oberbegriffe "T310 / 50" mit "T310" zusammen?

- Oberbegriffe Paillier vs Paillier Cryptosystem

- Oberbegriffe "Factorization with GNFS" vs "Factorization of a number"

### Functionality groups

ADFGVX -> ADFGX / ADFGVX

## Glossary

- "Functionality" vs "Path"
    - "Functionality" should be understood as a shorthand for "Functionality cluster" or "umbrella term" and translates to the german "Oberbegriff"
    - When referring to a specific thing, that a CrypTool offers to the user, prefer to refer to it as "Function", or better "Path" in the context of this project.
    - The "Path" of a function is something like "CT2:T \ Cryptanalysis \ Modern \ Differential Cryptanalysis Tutorial 1"
- "Category" should not be confused with the german "Oberbegriff". It simply is one of the dozen (1-14+) categories into which functionalities are categorized to be filtered by. Currently, a functionality is in exactly one Category.

# One path in CT2 corresponds to multiple functionalities

Currently

CT2 generates 

## These have been found to appear twice in the -GenerateFunctionList output

_vgl. ct2 output:_

Boolean Output;C/T;
;[T];Codes\ ISBN-10 Check
;[T];Codes\ ISBN-13 Check

(Funk.)=BoolOut;;[T];Codes\ ISBN-10 Check

Comparators;C/T;
;[T];Codes\ ISBN-10 Check
;[T];Codes\ ISBN-13 Check

(Funk.)=Comparators;;Codes\ ISBN-10 Check


CT2:dynamic:81208b59;<enter category here>;CT2:T \ Codes \ ISBN-10 Check
CT2:dynamic:c1144ed6;<enter category here>;CT2:T \ Codes \ ISBN-13 Check
CT2:dynamic:df766f5f;13) Protocols;CT2:T \ Protocols \ Diffie-Hellman Key-Exchange
CT2:dynamic:df766f5f;13) Protocols;CT2:T \ Protocols \ Diffie-Hellman Key-Exchange
CT2:dynamic:df766f5f;13) Protocols;CT2:T \ Protocols \ Diffie-Hellman Key-Exchange
CT2:dynamic:df766f5f;13) Protocols;CT2:T \ Protocols \ Diffie-Hellman Key-Exchange
CT2:dynamic:1bf13fcd;<enter category here>;CT2:T \ Cryptanalysis \ Modern \ Differential Cryptanalysis Tutorial 1
CT2:dynamic:1bf13fcd;<enter category here>;CT2:T \ Cryptanalysis \ Modern \ Differential Cryptanalysis Tutorial 1
CT2:dynamic:1bf13fcd;<enter category here>;CT2:T \ Cryptanalysis \ Modern \ Differential Cryptanalysis Tutorial 1
CT2:dynamic:1bf13fcd;<enter category here>;CT2:T \ Cryptanalysis \ Modern \ Differential Cryptanalysis Tutorial 1
CT2:dynamic:070870b6;<enter category here>;CT2:T \ Tools \ Keccak pseudorandom number generator (PRNG)
CT2:dynamic:39986255;6) Classic Cryptanalysis;CT2:T \ Cryptanalysis \ Classical \ Enigma Analyzer
CT2:dynamic:43c39728;<enter category here>;CT2:T \ Mathematics \ Next Smaller Prime Number
CT2:dynamic:4b42ed9a;<enter category here>;CT2:T \ Hash Functions \ Dictionary Attack on a password hash value
CT2:dynamic:4b42ed9a;<enter category here>;CT2:T \ Hash Functions \ Dictionary Attack on a password hash value
CT2:dynamic:4b42ed9a;<enter category here>;CT2:T \ Hash Functions \ Dictionary Attack on a password hash value
CT2:dynamic:4b42ed9a;<enter category here>;CT2:T \ Hash Functions \ Dictionary Attack on a password hash value
CT2:dynamic:4b42ed9a;<enter category here>;CT2:T \ Hash Functions \ Dictionary Attack on a password hash value
CT2:dynamic:5583b8d0;<enter category here>;CT2:T \ Cryptanalysis \ Modern \ Differential Cryptanalysis Tutorial 2 (automatic mode)
CT2:dynamic:5583b8d0;<enter category here>;CT2:T \ Cryptanalysis \ Modern \ Differential Cryptanalysis Tutorial 2 (automatic mode)
CT2:dynamic:5583b8d0;<enter category here>;CT2:T \ Cryptanalysis \ Modern \ Differential Cryptanalysis Tutorial 2 (automatic mode)
CT2:dynamic:5583b8d0;<enter category here>;CT2:T \ Cryptanalysis \ Modern \ Differential Cryptanalysis Tutorial 2 (automatic mode)
CT2:dynamic:6c89cceb;<enter category here>;CT2:T \ Experimental \ Encrypted VM (Simple Example)
CT2:dynamic:6d8f1007;<enter category here>;CT2:T \ Protocols \ Heartbleed Test
CT2:dynamic:6f0254d5;<enter category here>;CT2:T \ Cryptanalysis \ Modern \ Differential Cryptanalysis Tutorial 2
CT2:dynamic:6f0254d5;<enter category here>;CT2:T \ Cryptanalysis \ Modern \ Differential Cryptanalysis Tutorial 2
CT2:dynamic:6f0254d5;<enter category here>;CT2:T \ Cryptanalysis \ Modern \ Differential Cryptanalysis Tutorial 2
CT2:dynamic:6f0254d5;<enter category here>;CT2:T \ Cryptanalysis \ Modern \ Differential Cryptanalysis Tutorial 2
CT2:dynamic:734b4e59;<enter category here>;CT2:T \ Experimental \ SIGABA contraposition Analysis
CT2:dynamic:734b4e59;<enter category here>;CT2:T \ Experimental \ SIGABA contraposition Analysis
CT2:dynamic:73666a5e;<enter category here>;CT2:T \ Cryptanalysis \ Modern \ Differential Cryptanalysis Tutorial 3 (tutorial mode)
CT2:dynamic:73666a5e;<enter category here>;CT2:T \ Cryptanalysis \ Modern \ Differential Cryptanalysis Tutorial 3 (tutorial mode)
CT2:dynamic:73666a5e;<enter category here>;CT2:T \ Cryptanalysis \ Modern \ Differential Cryptanalysis Tutorial 3 (tutorial mode)
CT2:dynamic:73666a5e;<enter category here>;CT2:T \ Cryptanalysis \ Modern \ Differential Cryptanalysis Tutorial 3 (tutorial mode)
CT2:dynamic:75413309;3) Hash and MAC Algorithms;CT2:T \ Hash Functions \ CRC Null problems
CT2:dynamic:75ffe28d;<enter category here>;CT2:T \ Protocols \ Yao's Millionaire Problem Protocol
CT2:dynamic:75ffe28d;<enter category here>;CT2:T \ Protocols \ Yao's Millionaire Problem Protocol
CT2:dynamic:75ffe28d;<enter category here>;CT2:T \ Protocols \ Yao's Millionaire Problem Protocol
CT2:dynamic:75ffe28d;<enter category here>;CT2:T \ Protocols \ Yao's Millionaire Problem Protocol
CT2:dynamic:75ffe28d;<enter category here>;CT2:T \ Protocols \ Yao's Millionaire Problem Protocol
CT2:dynamic:765b9a28;<enter category here>;CT2:T \ Protocols \ Simple Multi Client Communication
CT2:dynamic:795e8949;<enter category here>;CT2:T \ Cryptanalysis \ Modern \ Differential Cryptanalysis Tutorial 1 (automatic mode)
CT2:dynamic:795e8949;<enter category here>;CT2:T \ Cryptanalysis \ Modern \ Differential Cryptanalysis Tutorial 1 (automatic mode)
CT2:dynamic:795e8949;<enter category here>;CT2:T \ Cryptanalysis \ Modern \ Differential Cryptanalysis Tutorial 1 (automatic mode)
CT2:dynamic:795e8949;<enter category here>;CT2:T \ Cryptanalysis \ Modern \ Differential Cryptanalysis Tutorial 1 (automatic mode)
CT2:dynamic:8551f5f9;<enter category here>;CT2:T \ Cryptanalysis \ Modern \ Differential Cryptanalysis Tutorial 3 (automatic mode)
CT2:dynamic:8551f5f9;<enter category here>;CT2:T \ Cryptanalysis \ Modern \ Differential Cryptanalysis Tutorial 3 (automatic mode)
CT2:dynamic:8551f5f9;<enter category here>;CT2:T \ Cryptanalysis \ Modern \ Differential Cryptanalysis Tutorial 3 (automatic mode)
CT2:dynamic:8551f5f9;<enter category here>;CT2:T \ Cryptanalysis \ Modern \ Differential Cryptanalysis Tutorial 3 (automatic mode)
CT2:dynamic:8b07fe29;<enter category here>;CT2:T \ Tools \ Take a Picture using the webcam
CT2:dynamic:93ff7e36;<enter category here>;CT2:T \ Experimental \ Encrypted VM (Machine Code Output)
CT2:dynamic:a09de055;<enter category here>;CT2:T \ Cryptanalysis \ Modern \ Differential Cryptanalysis Tutorial 2 (tutorial mode)
CT2:dynamic:a09de055;<enter category here>;CT2:T \ Cryptanalysis \ Modern \ Differential Cryptanalysis Tutorial 2 (tutorial mode)
CT2:dynamic:a09de055;<enter category here>;CT2:T \ Cryptanalysis \ Modern \ Differential Cryptanalysis Tutorial 2 (tutorial mode)
CT2:dynamic:a09de055;<enter category here>;CT2:T \ Cryptanalysis \ Modern \ Differential Cryptanalysis Tutorial 2 (tutorial mode)
CT2:dynamic:b09f171e;<enter category here>;CT2:T \ Experimental \ CypherMatrix Cipher (File Input)
CT2:dynamic:b09f171e;<enter category here>;CT2:T \ Experimental \ CypherMatrix Cipher (File Input)
CT2:dynamic:b78d06b0;<enter category here>;CT2:T \ Experimental \ Webhits for a hash value
CT2:dynamic:b78d06b0;<enter category here>;CT2:T \ Experimental \ Webhits for a hash value
CT2:dynamic:c08be9d1;<enter category here>;CT2:T \ Cryptanalysis \ Modern \ Differential Cryptanalysis Tutorial 1 (tutorial mode)
CT2:dynamic:c08be9d1;<enter category here>;CT2:T \ Cryptanalysis \ Modern \ Differential Cryptanalysis Tutorial 1 (tutorial mode)
CT2:dynamic:c08be9d1;<enter category here>;CT2:T \ Cryptanalysis \ Modern \ Differential Cryptanalysis Tutorial 1 (tutorial mode)
CT2:dynamic:c08be9d1;<enter category here>;CT2:T \ Cryptanalysis \ Modern \ Differential Cryptanalysis Tutorial 1 (tutorial mode)
CT2:dynamic:c7d0a3b4;<enter category here>;CT2:T \ Cryptanalysis \ Modern \ AES Analysis using Entropy (2) - with changeable plaintext
CT2:dynamic:c7d0a3b4;<enter category here>;CT2:T \ Cryptanalysis \ Modern \ AES Analysis using Entropy (2) - with changeable plaintext
CT2:dynamic:ce4a9661;<enter category here>;CT2:T \ Experimental \ Encrypted VM (Wrong Number of Cycles)
CT2:dynamic:d1d02228;6) Classic Cryptanalysis;CT2:T \ Cryptanalysis \ Classical \ Playfair Analysis
CT2:dynamic:d4ea7e1d;13) Protocols;CT2:T \ Experimental \ Bitcoin Blockchain Analysis
CT2:dynamic:d4ea7e1d;13) Protocols;CT2:T \ Experimental \ Bitcoin Blockchain Analysis
CT2:dynamic:d4ea7e1d;13) Protocols;CT2:T \ Experimental \ Bitcoin Blockchain Analysis
CT2:dynamic:e09bfa66;<enter category here>;CT2:T \ Mathematics \ Loop (1)
CT2:dynamic:e0c35294;<enter category here>;CT2:T \ Experimental \ SIGABA bruteforce Analysis
CT2:dynamic:e0c35294;<enter category here>;CT2:T \ Experimental \ SIGABA bruteforce Analysis
CT2:dynamic:e0c35294;<enter category here>;CT2:T \ Experimental \ SIGABA bruteforce Analysis
CT2:dynamic:e888bdf8;6) Classic Cryptanalysis;CT2:T \ Cryptanalysis \ Classical \ ADFGVX heuristic analysis
CT2:dynamic:efd62fe7;<enter category here>;CT2:T \ Cryptanalysis \ Modern \ Differential Cryptanalysis Tutorial 3
CT2:dynamic:efd62fe7;<enter category here>;CT2:T \ Cryptanalysis \ Modern \ Differential Cryptanalysis Tutorial 3
CT2:dynamic:efd62fe7;<enter category here>;CT2:T \ Cryptanalysis \ Modern \ Differential Cryptanalysis Tutorial 3
CT2:dynamic:efd62fe7;<enter category here>;CT2:T \ Cryptanalysis \ Modern \ Differential Cryptanalysis Tutorial 3
CT2:dynamic:f56e061e;<enter category here>;CT2:T \ Tools \ Download documents from the DECODE database
CT2:dynamic:fa86b2b3;<enter category here>;CT2:T \ Experimental \ Encrypted VM (Very long Execution Time)


# this may be in the wrong component/etc category in CT2

CT2:dynamic:472c4a23;6) Classic Cryptanalysis;CT2:C \ Tools \ Misc \ SigabaBruteforce
CT2:dynamic:a4872407;2) Modern Ciphers;CT2:C \ Tools \ Misc \ LFSR

# misc

"Was ist mit...?" --> entfernen?

CT2:dynamic:9f6dc562;14) Tools;CT2:C \ Tools \ Misc \ Example Plugin
