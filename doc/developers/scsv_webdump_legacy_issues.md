# Issues with the web-dumped data 

Original data that was manually dumped from cryptool.org is in data/scsv_webdump/original. This documents the issues that have been identified during development with that data. It was created manually at that time and has artifacts; most of it was resolved on-the-spot but some have been left untouched for reasons. This document keeps track of these issues, resolved and unresolved.

## scsv_webdump/CT2.csv @ CT2:static:82

### in scsv_CT2/FunctionList-en.csv

- missing path, nan

Artifact:

```
CT2:static:82;Coin Flipping Protocol;CT2:C\T;nan;10) Learning Aids and Visualizations
```

### in genCSV

```
Coin Flipping;C/T;
               ;[C];Protocols\ Coin Flipping
               ;[T];Protocols\ Coin Flipping Protocol
```

### in scsv_webdump/CT2.csv

```
Ciphertext-only;W  ;
               ;[W];Cryptanalysis\ Modern Encryption\ Symmetric Encryption\ AES\ Ciphertext-only
               ;[W];Cryptanalysis\ Modern Encryption\ Symmetric Encryption\ DES\ Ciphertext-only
               ;[W];Cryptanalysis\ Modern Encryption\ Symmetric Encryption\ SDES\ Ciphertext-only
```

### Status

repaired (path inserted into scsv_webdump/CT2.csv)

## scsv_webdump/CT2.csv @ CT2:static:417

- Missing field: path somewhere (renders csv invalid -- fixed)
- different number of entries, "on"/"against" AES or without AES (div)

```
CT2:static:18;AES;CT2:T;Cryptanalysis\ Modern\ Padding Oracle Attack on AES;2) Modern Ciphers
CT2:static:412;Padding Oracle;CT2:C;Tools\ Misc\ Padding Oracle;7) Modern Cryptanalysis
CT2:static:413;Padding Oracle;CT2:T;Cryptanalysis\ Modern\ Padding Oracle Attack on AES;7) Modern Cryptanalysis
CT2:static:415;Padding Oracle Attack against AES;CT2:C;Tools\ Misc\ Padding Oracle Attack;7) Modern Cryptanalysis
CT2:static:416;Padding Oracle Attack against AES;CT2:T;Cryptanalysis\ Modern\ Padding Oracle Attack on AES;7) Modern Cryptanalysis
CT2:static:417;Padding Oracle Attack against AES;CT2:C\T;;7) Modern Cryptanalysis
```

### in scsv_CT2/FunctionList-en.csv

```
AES;C/T/W;
;[T];Cryptanalysis\ Modern\ Padding Oracle Attack on AES
Padding Oracle;C/T;
;[C];Tools\ Misc\ Padding Oracle
;[T];Cryptanalysis\ Modern\ Padding Oracle Attack on AES
Padding Oracle Attack;C/T;
;[C];Tools\ Misc\ Padding Oracle Attack
;[T];Cryptanalysis\ Modern\ Padding Oracle Attack on AES
```

### Status

(1) missing path fixed with Tools\ Misc\ Padding Oracle Attack

(2) unresolved, seems like this is divergent

Another possibility is that the Misc Padding Oracle got renamed to represent both AES and DES?


## scsv_webdump/JCT.csv @ JCT:static:110

### in webdump

```
JCT:static:109;HMACs;JCT:A;[A] Message Authentication Codes\ Message Authentication Codes\ HmacSHA384;3) Hash and MAC Algorithms
JCT:static:109;HMACs;JCT:A;[A] Message Authentication Codes\ Message Authentication Codes\ HmacSHA384;3) Hash and MAC Algorithms
JCT:static:110;HMACs;JCT:A;;3) Hash and MAC Algorithms
```

### Status

- it is clear that HMAC512 is missing and HMAC384 is there two times; the missing path from context of the lines around (e.g. JCT:static:109) -- fixed

## scsv_webdump/JCT.csv @ JCT:static:54, 55

- missing how_implemented

```
JCT:static:54;Coin Flipping Protocol;JCT:;[C] Protocols\ Coin Flipping;10) Learning Aids and Visualizations
JCT:static:55;Coin Flipping Protocol;JCT:;[T] Protocols\ Coin Flipping Protocol;10) Learning Aids and Visualizations
```

### Status

- fixed by inferring from Path prefix

## scsv_webdump/JCT.csv @ 14

- Incomplete path

```
JCT:static:14;AES;JCT:D;[A] Block Ciphers\ Block Ciphers\ Rijndael;2) Modern Ciphers
```

### Status

fixed



## Similarly named entries (as notices while passing through)

- in scsv_CT2/FunctionList-en.csv: padding oracle on/against AES

```
CT2:static:18;AES;CT2:T;Cryptanalysis\ Modern\ Padding Oracle Attack on AES;2) Modern Ciphers
CT2:static:413;Padding Oracle;CT2:T;Cryptanalysis\ Modern\ Padding Oracle Attack on AES;7) Modern Cryptanalysis
CT2:static:415;Padding Oracle Attack against AES;CT2:C;Tools\ Misc\ Padding Oracle Attack;7) Modern Cryptanalysis
CT2:static:416;Padding Oracle Attack against AES;CT2:T;Cryptanalysis\ Modern\ Padding Oracle Attack on AES;7) Modern Cryptanalysis
CT2:static:417;Padding Oracle Attack against AES;CT2:C\T;;7) Modern Cryptanalysis
```

## JCT paths

JCT paths start with bracketed [D/a], unlike the paths of the other tools. in the output, CT2 tools need the prefix too.l
In SCSV format however, all paths are now prefixed with `(CT1|CT2|CTO|JCT):Letter:\ ` anyways.

for now, that seems like the SCSV have information heavily duplicated within JCT files. But it is for consistency.

## Merge and unmerge of MCSV in serialization/deserialization

MCSV: Because duplicate elements are deleted from each cell of a row when writing to csv ("Merge"), when reading them in again for further processing, the cells may not contain the same number of elements. they are however prefixed with the CrypTool id (CT1/2/O/J) for easier processing


## Sometimes, multiple Categories are assigned to one functionality

e.g. (from all_finalform.csv)

end of dataset: `10) Learning Aids and Visualizations <br \>13) Protocols`

more in detail:

```
|| Coin Flipping Protocol ['JCT:static:54', 'JCT:static:55', 'CT2:static:82', 'CT2:static:83']: ['10) Learning Aids and Visualizations', '13) Protocols']
|| Diffie-Hellman Key Exchange (Perfect Forward Secrecy) Visualization ['JCT:static:58', 'JCT:static:59', 'CT1:static:31', 'CT1:static:32']: ['10) Learning Aids and Visualizations', '13) Protocols']
|| RSA ['JCT:static:166', 'JCT:static:167', 'JCT:static:168', 'JCT:static:169', 'JCT:static:170', 'JCT:static:171', 'JCT:static:172', 'JCT:static:173', 'JCT:static:174', 'JCT:static:175', 'JCT:static:176', 'JCT:static:177', 'JCT:static:178', 'JCT:static:179', 'JCT:static:180', 'JCT:static:181', 'JCT:static:182', 'JCT:static:183', 'JCT:static:184', 'CT1:static:104', 'CT1:static:105', 'CT2:static:485', 'CT2:static:486', 'CT2:static:487', 'CT2:static:488', 'CT2:static:489', 'CT2:static:490', 'CT2:static:491', 'CT2:static:492', 'CT2:static:493', 'CT2:static:494', 'CT2:static:495', 'CT2:static:496', 'CT2:static:497', 'CT2:static:498', 'CT2:static:499']: ['2) Modern Ciphers', '4) Digital Signatures/PKI']
|| Shamir's Secret Sharing Visualization ['JCT:static:212', 'JCT:static:213', 'CT1:static:121', 'CT1:static:122']: ['10) Learning Aids and Visualizations', '13) Protocols']
|| Authentication Methods in Networks Visualization ['CT1:static:11', 'CT1:static:12']: ['10) Learning Aids and Visualizations', '13) Protocols']
|| Secure Email (S/MIME) Visualization ['CT1:static:113', 'CT1:static:114']: ['10) Learning Aids and Visualizations', '13) Protocols']
|| BB84 Key Exchange ['CT2:static:46', 'CT2:static:47', 'CT2:static:48', 'CT2:static:49', 'CT2:static:50', 'CT2:static:51', 'CT2:static:52', 'CT2:static:53', 'CT2:static:54']: ['10) Learning Aids and Visualizations', '13) Protocols']
|| BB84 Key Exchange with Eavesdropping Attack ['CT2:static:55', 'CT2:static:56']: ['10) Learning Aids and Visualizations', '13) Protocols']
|| Bit Commitment Scheme ['CT2:static:59', 'CT2:static:60', 'CT2:static:61', 'CT2:static:62']: ['7) Modern Cryptanalysis', '13) Protocols']
|| Dining Cryptographers Protocol ['CT2:static:257', 'CT2:static:258']: ['10) Learning Aids and Visualizations', '13) Protocols']
|| Oblivious Transfer Protocol ['CT2:static:404', 'CT2:static:405', 'CT2:static:406', 'CT2:static:407', 'CT2:static:408', 'CT2:static:409', 'CT2:static:410', 'CT2:static:411']: ['10) Learning Aids and Visualizations', '13) Protocols']
|| Virtual Smartcard ['CT2:static:600', 'CT2:static:601', 'CT2:static:602', 'CT2:static:603', 'CT2:static:604']: ['10) Learning Aids and Visualizations', '13) Protocols']
|| Wired Equivalent Privacy (WEP) ['CT2:static:628', 'CT2:static:629', 'CT2:static:630']: ['2) Modern Ciphers', '13) Protocols']
|| Yao's Millionaire Problem ['CT2:static:646', 'CT2:static:647', 'CT2:static:648', 'CT2:static:649', 'CT2:static:650', 'CT2:static:651', 'CT2:static:652', 'CT2:static:653']: ['10) Learning Aids and Visualizations', '13) Protocols']
|| Zero Knowledge Protocol ['CT2:static:654', 'CT2:static:655', 'CT2:static:656', 'CT2:static:657', 'CT2:static:658', 'CT2:static:659']: ['10) Learning Aids and Visualizations', '13) Protocols']
```

```
Shamir's Secret Sharing Visualization;X;;D;;Indiv. Procedures \ Secret Sharing Demonstration (Shamir)…;;[D] \ Visualizations \ Shamir's Secret Sharing <br /> [D] \ Visuals \ Shamir's Secret Sharing;;;10) Learning Aids and Visualizations <br \>13) Protocols
```

# Open issues

- many...
- Next up: CT2 paths do not have their prefix e.g. [T] \ ...
