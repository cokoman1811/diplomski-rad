# Što se točno događa u ovom projektu?

**Kratki vodič za razumijevanje diplomskog rada i programa**

Ako ti ništa nije jasno — pročitaj ovaj dokument od početka do kraja. Pisan je jednostavnim jezikom, bez pretpostavke da već znaš strojno učenje ili statistiku.

---

## 1. O čemu je rad u jednoj rečenici?

Imamo **puno mjerenja temperature** (svakih 10 minuta). Zamišljamo da imamo **samo svako 2., 3., 6. ili 12. mjerenje** — ostalo “nestane”. Program pokušava **pogoditi nestale vrijednosti** različitim metodama i usporedi **koja metoda najbolje pogada**.

---

## 2. Zašto uopće radimo ovo?

U stvarnom svijetu senzori ponekad ne šalju podatke redovito:

- rijetko mjerenje (štednja baterije),
- prekid veze,
- rupe u bazi podataka.

Pitanje rada je: **može li strojno učenje bolje popuniti te rupe od klasičnih metoda** (npr. crtanje ravne linije između dvije poznate točke)?

---

## 3. Koji podaci se koriste?

**Jena Climate dataset** — meteorološki podaci iz Jené (Njemačka), 2009.–2016.

- **Glavna varijabla:** temperatura zraka (°C)
- **Pomoćne varijable (covariates):** tlak, vlažnost, brzina vjetra
- **Učestalost:** otprilike svakih **10 minuta** jedno mjerenje

Podaci leže u: `data/raw/jena_climate_2009_2016.csv`

---

## 4. Ključni pojmovi (rječnik)

| Pojam | Značenje jednostavnim riječima |
|-------|--------------------------------|
| **Vremenska serija** | Niz brojeva poredan po vremenu (temperatura kroz dane/mjesece) |
| **Degradacija** | Namjerno “uklanjamo” dio podataka da simuliramo rupe |
| **Faktor degradacije** | Broj n: zadržimo svaki **n-ti** uzorak, ostalo je prazno (NaN) |
| **Interpolacija** | Popunjavanje praznina između poznatih točaka |
| **Rekonstrukcija** | Isto — vraćamo procijenjene vrijednosti na mjesta gdje su bile rupe |
| **Klasična metoda** | Pravilo bez učenja (npr. spoji točke ravnom linijom) |
| **Strojno učenje (ML)** | Model se **trenira** na dijelu podataka i onda predviđa praznine |
| **Train (treniranje)** | Razdoblje 2009.–2014. — tu model uči |
| **Test** | Razdoblje 2015.–2016. — tu **provjeravamo** točnost |
| **MAE** | Prosječna veličina greške (manje = bolje) |
| **RMSE** | Slično MAE, ali jače kažnjava velike greške |
| **R²** | Koliko dobro model objašnjava podatke (1 = savršeno, 0 = loše, negativno = vrlo loše) |

---

## 5. Što program radi — korak po korak

Kad pokreneš npr. `runfast.bat` ili `python main.py --quick --open-report`, događa se sljedeće:

### Korak 1 — Učitavanje podataka

Program učita CSV, postavi datum/vrijeme kao indeks i pripremi stupac `temperature` + pomoćne stupce.

### Korak 2 — Podjela na train i test

- **Train:** do kraja 2014. (model smije učiti samo ovdje)
- **Test:** 2015.–2016. (ovdje mjerimo točnost — kao “ispit”)

Zašto? Da vidimo radi li metoda i na **novom razdoblju**, a ne samo “pamti” prošlost.

### Korak 3 — Degradacija (pravljenje rupa)

Za svaki **faktor** (npr. 2, 6):

- zadrži se svaki 2. (ili 6., 12.) uzorak,
- sve ostalo postane **prazno (NaN)**.

Primjer s faktorom 2:

```
Original:     10  11  12  13  14  15  16  17
Degradirano:  10  NaN 12  NaN 14  NaN 16  NaN
```

Program **zna** original (tajne točke) samo da bi **ocijenio** metodu — metoda original ne smije “varati” gledati.

### Korak 4 — Rekonstrukcija (popunjavanje)

Za **svaku metodu** i **svaki faktor** program pokuša popuniti NaN vrijednosti.

**Klasične metode** (ne uče, samo primijene formula):

| Metoda | Ideja |
|--------|--------|
| Forward fill | Prepis zadnje poznate vrijednosti unaprijed |
| Linear | Ravna linija između susjednih poznatih točaka |
| Time | Linearno, ali po stvarnom vremenu između točaka |
| Cubic | Glatka krivulja (polinom) |
| Spline | Još glatkija krivulja između točaka |

**Metode strojnog učenja:**

| Metoda | Ideja |
|--------|--------|
| Random Forest | Mnogo stabala odluke; uči obrasce iz prošlih temperatura + vremena + vlažnosti/tlaka |
| MLP | Mala neuronska mreža na istim značajkama |

ML modeli se treniraju na **train** dijelu; predikcija ide na sva mjesta gdje je NaN.

### Korak 5 — Evaluacija (ocjenjivanje)

Program usporedi **procjenu** s **pravim originalom**, ali **samo**:

- na mjestima koja su bila uklonjena (rupe),
- u **testnom** razdoblju (2015.–2016.).

Računaju se **MAE**, **RMSE** i **R²**.

### Korak 6 — Spremanje rezultata

| Gdje | Što |
|------|-----|
| `results/tables/experiment_results.csv` | Glavna tablica: faktor × metoda × MAE/RMSE/R² |
| `results/figures/*.png` | Grafovi (rekonstrukcija, greške, usporedbe) |
| `results/report.html` | Pregled u browseru — tablice + slike po metodama |
| `results/tables/` (ostalo) | Rangovi, pivot tablice, tekst za tezu |

### Korak 7 — Ispis u terminalu

Lijepi sažetak: progress bar tijekom rada, tablica rezultata, najbolja metoda po faktoru, leaderboard.

### Korak 8 — HTML u browseru (ako `--open-report`)

Otvara se `report.html` s grupiranim grafikonima po metodama.

---

## 6. Što znače faktori 2, 3, 6, 12?

To je **koliko rijetko “mjerimo”**:

| Faktor | Značenje | Rupa |
|--------|----------|------|
| 2 | Svako 2. mjerenje | ~50% podataka nestane |
| 3 | Svako 3. | ~67% nestane |
| 6 | Svako 6. | ~83% nestane |
| 12 | Svako 12. | ~92% nestane |

**Što je faktor veći**, to je rekonstrukcija **teža** — greške obično rastu.

---

## 7. Kako čitati rezultate?

### U terminalu ili CSV-u

Traži red npr.:

```
faktor=6, metoda=linear, MAE=0.16, R²=0.99
```

- **Mala MAE** → dobra rekonstrukcija
- **R² blizu 1** → model prati oblik serije
- **Negativan R²** (npr. MLP) → model je lošiji od “pogodi prosjek”

### U HTML izvještaju

1. **Kartice “Najbolje metode po faktoru”** — tko pobjeđuje za svaki n
2. **Leaderboard** — tko je ukupno najbolji
3. **Galerija po metodama** — vizualno kako svaka metoda popunjava rupe
4. Najvažniji graf: **Rekonstrukcija** — tri linije:
   - plava/original = istina
   - točkice = što je ostalo nakon degradacije
   - treća linija = što je metoda pogodila

### Tipičan zaključak ovog projekta

Na temperaturi Jena, za faktore 2–12, **jednostavne klasične metode** (linear, time, cubic) često imaju **manju MAE** od ML modela — temperatura je relativno glatka, a ML treba dobar tuning i dovoljno podataka.

To **nije greška u programu** — to je **znanstveni rezultat** rada.

---

## 8. Brzi vs puni run

| Naredba | Što radi |
|---------|----------|
| `runfast.bat` | Manji uzorak podataka, faktori **2 i 6**, brže (~10–30 s) |
| `run.bat` | **Cijeli** dataset, faktori **2, 3, 6, 12**, s ML tuningom (nekoliko minuta) |

Opcije:

- `--no-tune` — preskoči GridSearch (brže, ML lošiji)
- `--no-plots` — bez PNG grafova
- `--open-report` — otvori HTML nakon runa

---

## 9. Što su oni warnings u terminalu?

Poruka poput:

```
Skipping features without any observed values: ['lag_1' 'lag_2']
```

Znači: kod ML modela neke “prošle temperature” (lag značajke) su prazne na početku serije — sklearn ih preskoči. **Program radi dalje.** Nije crash.

---

## 10. Mapa projekta (gdje je što)

```
diplomski rad/
├── main.py              ← pokretanje (koristi .venv automatski)
├── runfast.bat          ← brzi run + browser
├── run.bat              ← puni run + browser
├── open_report.bat      ← samo otvori HTML
├── src/                 ← sav kod
├── data/raw/            ← Jena CSV
├── results/tables/      ← CSV rezultati
├── results/figures/     ← PNG grafovi
├── results/report.html  ← pregled u browseru
├── documentation/       ← tehnička dokumentacija po modulima
└── docs/                ← odluke, workflow, napredak rada
```

---

## 11. Logički tok — slika u glavi

```
Jena temperatura (puna serija)
        │
        ▼
   Degradacija (faktor n)
        │
        ├── poznate točke (svaki n-ti)
        └── praznine (NaN) ← ovo metode moraju popuniti
        │
        ▼
   Metoda (linear, RF, …)
        │
        ▼
   Rekonstruirana serija
        │
        ▼
   Usporedba s originalom (samo test + samo rupe)
        │
        ▼
   MAE, RMSE, R² → tablice, grafovi, HTML
```

---

## 12. Što dalje za diplomski?

1. Pokreni **puni run**: `run.bat`
2. Otvori **`results/report.html`** i odaberi grafove za rad
3. Koristi **`results/tables/`** za tablice u Word/LaTeX
4. Napiši poglavlja: uvod → metodologija (koraci iz ovog dokumenta) → rezultati → zaključak

---

## 13. Gdje tražiti više detalja?

| Dokument | Sadržaj |
|----------|---------|
| **Ovaj file** | Objašnjenje “što se događa” jednostavnim jezikom |
| [README.md](README.md) | Index tehničke dokumentacije |
| [03-tok-eksperimenta.md](03-tok-eksperimenta.md) | Detaljan tok u kodu |
| [docs/project.md](../docs/project.md) | Službeni opis rada |
| [docs/decisions.md](../docs/decisions.md) | Zašto su odabrane metode i postavke |

---

## 14. Najkraći mogući sažetak

1. Uzmemo punu temperaturu iz Jene.  
2. Namjerno izbacimo dio mjerenja (faktor 2/3/6/12).  
3. Svaka metoda pokuša vratiti izgubljeno.  
4. Mjerimo grešku na skrivenim točkama u 2015.–2016.  
5. Spremimo tablice i grafove i pokažemo tko je najbolji.  

**Cilj rada:** utvrditi jesu li klasične metode dovoljne ili ML donosi prednost — na ovom datasetu i ovom eksperimentu.

---

*Ako nešto i dalje nije jasno, pitaj konkretno (npr. “što je lag značajka” ili “zašto je R² negativan”) — lakše je objasniti jedan dio nego cijeli projekt odjednom.*
