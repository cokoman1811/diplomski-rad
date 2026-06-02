# Progress log

## Current status

Full thesis pipeline implemented: data loading, degradation, classical and ML methods, evaluation, statistical analysis, plots, experiment runner and tests.

Next step: run full experiments and write thesis chapters from saved results.

---

## Completed tasks

### Project setup

- [x] Git repository created
- [x] Python virtual environment created
- [x] Project structure created
- [x] AGENTS.md and docs/ created
- [x] requirements.txt and requirements-dev.txt added

### Dataset

- [x] Jena Climate dataset downloaded to `data/raw/`
- [x] `src/data_loader.py` implemented
- [x] Covariate loading implemented

### Core pipeline

- [x] `src/config.py` implemented
- [x] `src/preprocessing.py` implemented
- [x] `src/interpolation_methods.py` implemented
- [x] `src/feature_engineering.py` implemented
- [x] `src/ml_models.py` implemented
- [x] `src/hyperparameter_tuning.py` implemented
- [x] `src/evaluation.py` implemented
- [x] `src/statistical_analysis.py` implemented
- [x] `src/plots.py` implemented
- [x] `src/experiment_runner.py` implemented
- [x] `src/io_utils.py` implemented
- [x] CLI `main.py` implemented
- [x] Legacy prototype moved to `legacy/synthetic_prototype.py`

### Tests

- [x] `tests/` suite added
- [x] Extended grid, thesis notes and chapter generator tests added (~250 tests)

### Codebase size

- [x] Expanded supporting modules toward ~4000 LOC target (~4060 Python lines in src/, tests/, legacy/, main.py)

### Results

- [x] Baseline full experiment completed (`python main.py --run-all --no-tune`)
- [x] Result tables saved in `results/tables/`
- [x] Figures saved in `results/figures/`
- [x] Result notes written in `docs/results_notes.md`
- [ ] Final experiment with ML tuning completed

### Thesis writing

- [x] `src/thesis_chapters.py` — chapter skeleton and Croatian methodology text generators
- [x] `src/experiment_protocol.py` — reproducible experiment protocol documentation
- [x] `src/console.py` — estetski CLI ispis (banner, progress bar, tablice, boje)
- [x] `src/report_html.py` — HTML viewer (`results/report.html`) nakon svakog runa
- [x] `documentation/` — puna tehnička dokumentacija modula i toka programa
- [x] `documentation/STO-SE-DOGADA.md` — uvod i objašnjenje cijelog projekta za početnike
- [ ] Thesis chapters written
