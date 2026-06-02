# Testovi i legacy kod

## `tests/`

Pytest suite (~270 testova). Pokretanje:

```powershell
python -m pytest tests/
python -m pytest tests/ -q
```

### Glavne test datoteke

| Datoteka | Testira |
|----------|---------|
| `conftest.py` | Fixture: sintetička temperatura, sample results |
| `test_preprocessing.py` | Degradacija serije |
| `test_interpolation_methods.py` | Klasične metode |
| `test_feature_engineering.py` | Značajke i mask |
| `test_ml_models.py` | RF i MLP pipeline |
| `test_evaluation.py` | MAE, RMSE, R² |
| `test_experiment_runner.py` | Integracija runnera |
| `test_report_html.py` | HTML generator |
| `test_console.py` | Formatiranje tablica |
| `test_cli_helpers.py` | CLI pomoćne naredbe |
| `test_pipeline_grid.py` | Parametrizirani grid testovi |
| `test_thesis_chapters.py` | Generator poglavlja |
| `test_method_thesis_notes.py` | Opisi metoda |

Testovi koriste sintetičke podatke — ne treba pun Jena dataset za većinu testova.

## `legacy/synthetic_prototype.py`

Stari prototip eksperimenta na **sintetičkim** podacima (prije Jena pipelinea).

- **Ne koristi se** u glavnom `main.py`
- Zadržan kao arhiva ranijeg pristupa
- Ne proširivati za thesis pipeline

## Zašto toliko testova

Projekt ima ~5000 linija koda; testovi osiguravaju da promjene u jednom modulu ne razbiju degradaciju, metrike ili izvoz rezultata.

## CI / pre-commit

Trenutno nema GitHub Actions u repozitoriju — testove pokrećeš lokalno prije commita.
