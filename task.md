# Python víkend v Kiwi.com - vstupní úkol

Pomocí této úlohy nám prokážete, že jste s Pythonem již přišli do styku a znáte jeho základy. Tím pádem by nemělo nic bránit tomu, abyste si workshop užili a nebyl pro vás příliš složitý.

##Limitace

Žádné limitace.

- Python2.7 nebo 3
- všechny moduly jsou povoleny


##Popis úkolu

Máte data o jednotlivých letech (segmentech). Vaším úkolem je nalézt kombinace jednotlivých letů (itineráře, tzn. minimálně 2 segmenty) tak,
aby segmenty navazovaly s časem na přestup 1-4 hodiny. Jednotlivé sloupce jsou ve vstupních datech pojmenovány `source`, `destination` vyjadřující kód letiště odletu a příletu, `departure`, `arrival` jsou pak časy odletu a příletu (YYYY-MM-DD). Jakožto unikátní identifikátor segmentu slouží `flight_number`.

##Vstupní data (csv) (pouze ukázka)

```
source,destination,departure,arrival,flight_number
USM,HKT,2016-10-11T10:10:00,2016-10-11T11:10:00,PV511
USM,HKT,2016-10-11T18:15:00,2016-10-11T19:15:00,PV476
USM,HKT,2016-10-11T21:25:00,2016-10-11T22:25:00,PV281
USM,HKT,2016-10-11T14:10:00,2016-10-11T15:10:00,PV909
USM,HKT,2016-10-11T19:45:00,2016-10-11T20:45:00,PV310
USM,HKT,2016-10-11T21:35:00,2016-10-11T22:35:00,PV472
USM,HKT,2016-10-11T10:30:00,2016-10-11T11:30:00,PV913
USM,HKT,2016-10-11T11:45:00,2016-10-11T12:45:00,PV260
USM,HKT,2016-10-11T13:00:00,2016-10-11T14:00:00,PV719
HKT,USM,2016-10-11T16:00:00,2016-10-11T16:55:00,PV493
HKT,USM,2016-10-11T05:15:00,2016-10-11T06:10:00,PV870
HKT,DPS,2016-10-11T13:10:00,2016-10-11T16:50:00,PV967
HKT,USM,2016-10-11T10:00:00,2016-10-11T10:55:00,PV320
HKT,USM,2016-10-11T22:05:00,2016-10-11T23:00:00,PV551
HKT,USM,2016-10-11T13:40:00,2016-10-11T14:35:00,PV540
HKT,USM,2016-10-11T14:30:00,2016-10-11T15:25:00,PV444
BWN,DPS,2016-10-11T13:15:00,2016-10-11T15:35:00,PV189
BWN,DPS,2016-10-11T14:35:00,2016-10-11T16:55:00,PV477
BWN,DPS,2016-10-11T18:45:00,2016-10-11T21:05:00,PV923
BWN,DPS,2016-10-11T21:50:00,2016-10-12T00:10:00,PV541
BWN,DPS,2016-10-11T16:15:00,2016-10-11T18:35:00,PV811
BWN,DPS,2016-10-11T21:30:00,2016-10-11T23:50:00,PV949
BWN,DPS,2016-10-11T10:35:00,2016-10-11T12:55:00,PV996
BWN,DPS,2016-10-11T19:00:00,2016-10-11T21:20:00,PV612
DPS,HKT,2016-10-11T20:10:00,2016-10-11T23:50:00,PV731
DPS,BWN,2016-10-11T05:40:00,2016-10-11T08:05:00,PV332
DPS,HKT,2016-10-11T02:05:00,2016-10-11T05:45:00,PV697
DPS,BWN,2016-10-11T13:50:00,2016-10-11T16:15:00,PV534
DPS,HKT,2016-10-11T00:30:00,2016-10-11T04:10:00,PV606
DPS,HKT,2016-10-11T09:20:00,2016-10-11T13:00:00,PV980
DPS,BWN,2016-10-11T00:50:00,2016-10-11T03:15:00,PV184
```

##Výstup


- Výstupní data můžou být v jakémkoliv formátu vhodném k dalšímu zpracování.
- Ignorovat opakování segmentů (A->B) v kombinaci. A a B představují kód lětiště.
  - A->B->A->B je nevalidní kombinace. 
  - A->B->A je validní kombinace.

##Použití

Vstupní data bude program číst ze `stdin` a bude jej tak možné spustit následujícím způsobem `cat input.csv | find_combinations.py` skript poté zapíše výstup na `stdout` a případné chyby na `stderr`.

##Kontakt

- Posílat můžete jako .py soubor / .zip balík v příloze e-mailu nebo odkaz na GitHub repozitář.
- Vyřešené úkoly a otázky nám zasílejte na mike@kiwi.com
