# Workflow

## Daily workflow

1. Open Cursor.
2. Read AGENTS.md.
3. Read all files inside docs/.
4. Work on one small task at a time.
5. Run the code if possible.
6. Save results.
7. Update docs/progress.md.
8. If a technical decision was made, update docs/decisions.md.
9. Suggest a git commit message.

## Agent rules

Before writing code:

- explain the plan
- mention which files will be changed
- wait for confirmation if the change is large

After writing code:

- summarize changes
- mention how to run the code
- mention what should be tested
- update documentation

## Current run command

python main.py

Load Jena Climate data:

python -m src.data_loader

## Main project phases

1. Project setup
2. Data loading
3. Simulated degradation
4. Classical interpolation
5. Evaluation
6. Machine learning models
7. Plots and results
8. Thesis writing
