# Metode interpolacije i strojno učenje

## `src/interpolation_methods.py`

Klasične metode rekonstrukcije:

| Metoda | Opis |
|--------|------|
| `forward_fill` | Prepis zadnje poznate vrijednosti |
| `linear` | Linearna interpolacija između susjeda |
| `time` | Interpolacija po stvarnom vremenskom razmaku |
| `cubic` | Kubni polinom |
| `spline` | Spline krivulja |

`interpolate(series, method)` — jedinstvena funkcija za sve klasične metode.

## `src/feature_engineering.py`

Priprema značajke za ML:

- **lagovi** temperature (`lag_1`, `lag_2`, …)
- **rolling** statistike (prosjek, std)
- **cikličko vrijeme** (sat, dan, mjesec)
- **covariates** iz Jena dataseta

Funkcije:

- `build_feature_matrix()` — cijela matrica značajki
- `build_train_test_masks()` — train do 2014., test od 2015.
- `get_training_rows()` / `get_prediction_rows()` — redovi za fit i predikciju

## `src/ml_models.py`

- `reconstruct_with_ml()` — trenira RF ili MLP pipeline
- Pipeline: `SimpleImputer` → `StandardScaler` → model
- Vraća rekonstruiranu seriju i korištene hiperparametre

## `src/hyperparameter_tuning.py`

- `GridSearchCV` + `TimeSeriesSplit`
- Odvojene mreže parametara za Random Forest i MLP (`config.py`)
- Poziva se samo kad `tune_ml=True` i params još nisu cacheirani

## `src/method_info.py`

Metapodaci metoda (ime, kategorija, opis, koristi li covariates).

- `METHOD_DESCRIPTIONS` — rječnik za sve metode
- `CROATIAN_THESIS_NOTES` / `ENGLISH_THESIS_NOTES` — tekst za rad
- `build_bilingual_method_appendix()` — markdown za prilog

## Kada klasične pobjeđuju ML

Na glatkoj temperaturnoj seriji s malim gapovima (faktor 2–6), jednostavna interpolacija često ima manju MAE od ML-a. ML postaje konkurentniji kod većih faktora degradacije i kad su dobro namješteni hiperparametri.
