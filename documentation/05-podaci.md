# Podaci — učitavanje, validacija, degradacija

## `src/config.py`

Konstante projekta:

- putanje i imena stupaca Jena CSV-a
- `DEGRADATION_FACTORS = [2, 3, 6, 12]`
- liste klasičnih i ML metoda
- train/test datumi (`TRAIN_END`, `TEST_START`)
- hiperparametri za GridSearch (`RF_PARAM_GRID`, `MLP_PARAM_GRID`)

## `src/paths.py`

Standardne putanje:

- `DATA_DIR`, `RAW_DIR`, `RESULTS_DIR`, `TABLES_DIR`, `FIGURES_DIR`
- `ensure_project_dirs()` — kreira mape ako ne postoje

## `src/download_data.py`

- Preuzima Jena zip s Google Storage URL-a
- Raspakuje u `data/raw/jena_climate_2009_2016.csv`
- `ensure_jena_data()` — preuzmi samo ako nedostaje, validiraj stupce

## `src/data_loader.py`

- `load_jena_dataset()` — učitaj CSV, parsiraj datetime index
- Vraća DataFrame s `temperature` i covariates (tlak, vlažnost, vjetar)

## `src/validation.py`

- Provjera postojanja datoteke i obaveznih stupaca
- `validate_dataset_frame()` — baca `ValidationError` ako struktura nije ispravna

## `src/data_quality.py`

Izvještaj o kvaliteti podataka:

- missing values po stupcu
- veliki vremenski gapovi
- duplikati timestampa
- raspon temperature i covariates
- `full_quality_report()` — koristi CLI `check-data`

## `src/preprocessing.py`

### `degrade_series(series, factor)`

Zadrži svaki n-ti uzorak; ostalo postavi na `NaN`.

Vraća `DegradedSeries`:

- `original` — netaknuta serija
- `degraded` — serija s NaN na uklonjenim mjestima
- `removed_mask` — bool maska uklonjenih točaka
- `factor` — faktor degradacije

### `evaluation_mask(removed_mask, test_mask)`

Određuje točke za evaluaciju (uklonjene ∩ test).

### `slice_dataset_recent()`

Reže dataset na zadnjih N redaka (quick mode).

## `src/download_real_weather_data.py`

Alternativni/skriptni download (stariji pristup). Glavni pipeline koristi `download_data.py`.
