# more issues (others in old doc in ~/Documents)

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

JCT paths start with bracketed [D/a], unlike the paths of the other tools.
In SCSV format however, all paths are now prefixed with `(CT1|CT2|CTO|JCT):Letter:\ ` anyways.

for now, that seems like the SCSV have information heavily duplicated within JCT files. But it is for consistency.

## Merge and unmerge of MCSV in serialization/deserialization

MCSV: Because duplicate elements are deleted from each cell of a row when writing to csv ("Merge"), when reading them in again for further processing, the cells may not contain the same number of elements. they are however prefixed with the CrypTool id (CT1/2/O/J) for easier processing


