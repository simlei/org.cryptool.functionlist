core-developer sln

Raus: 
- bitcoin
- blockmode / <space>mode/modus
- CypherMatrix
- nfs/gnfs factorizer
- SIGABA-Analyse
- Verschlüsselte VM
- webtreffer

# TODO von ganz oben

## offen @ 27.01.


- Online bringen (Fehler mit de/Pfaden)
- Änderung in CT1 erforderlich, Test was passiert, wenn sich Pfad ändert
- ??: s. screenshot

Später
- Datenbanken migrieren

## Format: 

[x] - "XXX-Analyse"  (also mit Bindestrich) also Caesar-Analyse, Transpositions-Analyse, ...
[x] - "X Y -- Analyse"
[x] - Ja, bitte vereinheitlichen. "visual" gefällt mir besser, aber Hauptsache einheitlich.

** Fallbeispiele **

[x] - Magic door - Visualisierung ==> Magic door -- Visualisierung
[x] - Matrix-Bildschirmschoner-Visualisierung ==> Matrix-Bildschirmschoner -- Visualisierung
[x] - "Matrix"-Zeile die nicht mehr in CTO drin ist


## Inhalt:

[x] - Transposition analysis;Transpositions-Analyse
[x] - Homophonic substitution analysis;Homophone Substitutions-Analyse
[x] - Kryptos K1 analysis;Kryptos K1 -- Analyse
[x] - Kryptos K2 analysis;Kryptos K2 -- Analyse
[x] - Classical ciphers -- analysis;Klassische Verfahren -- Analyse
[x] - Homophonic substitution cipher ==> Homophone Substitutions-Chiffre
[x] - Bitte die ff. beiden lassen (also nicht zusammenfassen)
    [x] Transposition (ein-stufige Spaltentransposition)
    [x] Transposition (zwei-stufige Spaltentransposition) (Doppelwürfel)
[x] - 3DES Brute-Force-Angriff ==> 3DES-Angriff
[x] - AES Brute-Force-Angriff ==> AES-Angriff
[x] - DES Brute-Force-Angriff ==> DES-Angriff
[x] - DESL Brute-Force-Angriff ==> DESL-Angriff
[x] - DESX Brute-Force-Angriff ==> DESX-Angriff
[x] - DESXL Brute-Force-Angriff ==> DESXL-Angriff
[x] - 3DES und Triple-DES müssen wir bei den Funktionsnamen auch noch zusammen fassen.
[x] - Base 64 decodieren => Base 64 decodieren/encodieren
[x] - Base 64 encodieren => Base 64 decodieren/encodieren
[x] - Eindeutschen: PKCS#1 attack  -->  PKCS#1-Angriff

[x] SAT solver  ==>  SAT-Solver

- [x] Bitte die ff. beiden lassen (also nicht zusammenfassen)
    - Transposition (ein-stufige Spaltentransposition)
    - Transposition (zwei-stufige Spaltentransposition) (Doppelwürfel)
- [x] 3DES und Triple-DES müssen wir bei den Funktionsnamen auch noch zusammen fassen.

## Issues jetzt:

[x] - CT1/O Datensatz neu lesen für DE. Bsp das weg sein muss: "Matrix-Bildschirmschoner-Visualisierung"
[x] - Replay aller Anpassungen die auf dem alten de_ Dump passiert sind
[x] - Früher hatten wir (wie es in der Legende unten steht) in Spalte 2 (CT1) und 5 (CTO) jeweils ein x, wenn es einen Pfad gab. Dieses x haben Sie verloren.

## Issues später:

[x] - "3DES" filtering geht nicht
[x] - 368 Zeilen gefunden, die dem Auswahlkriterium entsprechen. ==> 368 Zeilen mit xxx Einträgen gefunden, die dem Auswahlkriterium entsprechen.

