# Izlaz — grafovi, tablice, HTML, thesis export

## `src/plots.py`

Generira PNG u `results/figures/` (backend `Agg`, bez GUI prozora).

| Funkcija | Graf |
|----------|------|
| `plot_reconstruction_window` | Original vs degradirano vs rekonstruirano |
| `plot_metric_bars` | Bar chart MAE/RMSE/R² po metodi |
| `plot_metric_heatmap` | Heatmap metrika |
| `plot_error_boxplot` | Boxplot grešaka po metodi |
| `plot_error_by_hour/month` | Greška po satu / mjesecu |
| `plot_residual_scatter` | Scatter residuala |
| `plot_error_histogram` | Histogram grešaka |
| `plot_all_factor_rankings` | Rang po faktoru |
| `plot_all_metric_lines` | Linijski trend metrika |

## `src/reporting.py`

- Markdown izvještaji (`experiment_report.md`)
- rangirane tablice, best method, classical vs ML
- `save_all_reports()` — sve odjednom
- `update_results_notes_template()` — ažurira `docs/results_notes.md`

## `src/report_html.py`

Generira **`results/report.html`**:

- kartice najboljih metoda
- leaderboard
- HTML tablica rezultata
- galerija grafova s JavaScript filterima
- **grupiranje po metodama** — naslov sekcije + svi grafikoni te metode, zatim sljedeća metoda
- linkovi na CSV

`open_html_report()` — otvara u browseru (`os.startfile` na Windowsu).

Header **nije sticky** — skrola se s ostatkom stranice.

## `src/thesis_export.py`

Izvoz tablica i rečenica za pisanje rada:

- pivot tablice (MAE, RMSE, R²)
- thesis_ranked_results, thesis_best_methods, thesis_leaderboard
- `build_croatian_summary_sentences()` — gotove rečenice za poglavlje Rezultati

## `src/thesis_chapters.py`

Generator skeleton teksta rada (HR):

- outline poglavlja
- metodologija, uvod, zaključak
- `build_full_thesis_skeleton(results)` — cijeli markdown draft

## `src/io_utils.py`

- `save_results_table()` — CSV u `results/tables/`
- `save_json()` — JSON rezultati

## `src/experiment_protocol.py`

Formalni opis koraka eksperimenta (protokol za metodologiju u radu).

## Gdje tražiti rezultate

| Datoteka | Sadržaj |
|----------|---------|
| `experiment_results.csv` | Glavna tablica |
| `report.html` | Pregled u browseru |
| `results/figures/*.png` | Svi grafovi |
| `thesis_summary_sentences.txt` | Tekst za rad |
