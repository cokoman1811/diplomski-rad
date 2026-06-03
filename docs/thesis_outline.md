# Thesis outline

## 1. Uvod

U ovom poglavlju treba objasniti:
- zašto su vremenski nizovi važni
- zašto su nedostajuće vrijednosti problem
- zašto je interpolacija korisna
- što je cilj diplomskog rada
- koje metode se uspoređuju
- kako je rad strukturiran

Cilj poglavlja:
Objasniti motivaciju rada i dati čitatelju pregled teme.

---

## 2. Vremenski nizovi

U ovom poglavlju treba objasniti:
- što je vremenski niz
- što znači vremenska rezolucija
- razlika između pravilnog i nepravilnog uzorkovanja
- primjeri vremenskih nizova: temperatura, potrošnja energije, senzorski podaci
- zašto je važno imati podatke u pravilnim vremenskim intervalima

Cilj poglavlja:
Uvesti osnovne pojmove potrebne za razumijevanje rada.

---

## 3. Interpolacija i imputacija podataka

U ovom poglavlju treba objasniti:
- što je interpolacija
- što je imputacija
- razlika između interpolacije, imputacije i predviđanja
- zašto se pojavljuju nedostajuće vrijednosti
- kako nedostajuće vrijednosti utječu na analizu podataka

Cilj poglavlja:
Objasniti problem koji diplomski rad rješava.

---

## 4. Klasične metode interpolacije

U ovom poglavlju treba opisati:
- forward fill
- linearna interpolacija
- time interpolation
- cubic interpolation
- spline interpolation

Za svaku metodu napisati:
- osnovnu ideju
- prednosti
- mane
- kada metoda može dobro raditi
- kada metoda može biti loša

Cilj poglavlja:
Objasniti baseline metode koje će se usporediti s metodama strojnog učenja.

---

## 5. Metode strojnog učenja

U ovom poglavlju treba opisati:
- Random Forest Regressor
- MLP Regressor
- ulazne značajke za modele
- zašto ML može pomoći kod rekonstrukcije vrijednosti

Ulazne značajke mogu biti:
- prethodna poznata vrijednost
- sljedeća poznata vrijednost
- udaljenost od prethodne poznate vrijednosti
- udaljenost do sljedeće poznate vrijednosti
- sat u danu
- dan u godini

Cilj poglavlja:
Objasniti metode strojnog učenja korištene u praktičnom dijelu.

---

## 6. Korišteni skup podataka

U ovom poglavlju treba opisati:
- Jena Climate dataset
- vremensku rezoluciju podataka
- koje varijable dataset sadrži
- zašto je dataset prikladan za ovu temu
- zašto se koristi temperatura kao ciljna varijabla

Cilj poglavlja:
Objasniti podatke nad kojima se provodi eksperiment.

---

## 7. Metodologija eksperimenta

U ovom poglavlju treba objasniti:
- učitavanje originalnih podataka
- umjetno prorjeđivanje vremenskog niza
- faktore prorjeđivanja 2, 3, 6 i 12
- stvaranje missing vrijednosti
- rekonstrukciju uklonjenih vrijednosti
- evaluaciju samo na umjetno uklonjenim vrijednostima

Cilj poglavlja:
Jasno opisati kako je eksperiment proveden.

---

## 8. Evaluacijske metrike

U ovom poglavlju treba opisati:
- MAE
- RMSE
- R2 score

Za svaku metriku napisati:
- što mjeri
- kako se interpretira
- zašto je korisna u ovom radu

Cilj poglavlja:
Objasniti kako se uspješnost metoda mjeri.

---

## 9. Rezultati

U ovom poglavlju treba prikazati:
- tablice rezultata
- grafove usporedbe metoda
- MAE po metodama
- RMSE po metodama
- R2 po metodama
- usporedbu originalnog i rekonstruiranog vremenskog niza

Cilj poglavlja:
Prikazati konkretne rezultate eksperimenta.

---

## 10. Rasprava

U ovom poglavlju treba objasniti:
- koja metoda je ostvarila najbolje rezultate
- kako se pogreška mijenja s povećanjem faktora prorjeđivanja
- kada su klasične metode dovoljne
- kada metode strojnog učenja imaju smisla
- zašto kompleksnija metoda nije uvijek bolja
- ograničenja provedenog eksperimenta

Cilj poglavlja:
Pokazati razumijevanje rezultata, a ne samo prikazati brojeve.

---

## 11. Zaključak

U ovom poglavlju treba napisati:
- što je napravljeno u radu
- koje metode su uspoređene
- koji su glavni zaključci
- koja su ograničenja rada
- što se može napraviti u budućem radu

Cilj poglavlja:
Sažeti cijeli rad i zaključiti što je pokazano eksperimentom.

---

## 12. Literatura

U ovom poglavlju treba dodati izvore za:
- vremenske nizove
- interpolaciju
- imputaciju
- Random Forest
- MLP / neuronske mreže
- evaluacijske metrike
- Jena Climate dataset

Napomena:
Ne izmišljati izvore. Ako izvor fali, označiti s:

[TODO: citation needed]
