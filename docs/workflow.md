# Workflow

## Purpose

This file defines the daily workflow for working on this master's thesis project with Cursor.

The goal is to work in small steps, keep the project organized, update documentation regularly, and avoid unnecessary complexity.

---

## Daily workflow

Every work session should follow these steps:

1. Open the project folder in Cursor.
2. Open Cursor Agent chat.
3. Ask the agent to read `AGENTS.md` and all files in `docs/`.
4. Ask the agent to summarize the current project state.
5. Work on only one small task at a time.
6. Run the code if possible.
7. Check if the output is correct.
8. Update `docs/progress.md`.
9. Update `docs/decisions.md` if a new technical decision was made.
10. Check `git status`.
11. Commit only clean and meaningful changes.
12. Push to GitHub when the work is stable.

---

## Start-of-chat prompt

At the beginning of every new Cursor chat, use this prompt:

```text
Read AGENTS.md and all files in docs/ before doing anything.

Then summarize:
1. what this project is about
2. what is already completed
3. what the next unfinished task is
4. which files should be changed next

Do not write code yet.

---

## Run commands

Load shortcuts in PowerShell:

```powershell
. .\shortcuts.ps1
runfast
run
```

| Command | What it runs |
|---------|----------------|
| `runfast` | `python main.py --quick` |
| `run` | `python main.py --run-all` |

Manual commands:

```powershell
python main.py --quick
python main.py --run-all
python main.py --run-all --no-tune
python -m pytest tests/
python -m src.data_loader
```

CLI output is formatted by `src/console.py`: banner, configuration summary, progress bar, result tables, leaderboard and saved file list. Colors use `colorama`; Unicode box drawing falls back to ASCII when needed.

After each experiment run, `results/report.html` is generated automatically. Open it in a browser to browse figures, metrics and CSV links. Use `--open-report` to open it automatically:

```powershell
python main.py --quick --open-report
```

Full technical documentation (all modules, file-by-file): see the [`documentation/`](../documentation/README.md) folder.

---