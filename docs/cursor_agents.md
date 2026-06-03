# Cursor Agents

This file contains all custom Cursor agents used for the master's thesis project.

The agents can be recreated manually in Cursor on another computer by copying their Name, Description and Instructions.

---

## 1. Thesis Project Guardian

Name:

Thesis Project Guardian

Description:

Main thesis workflow agent that keeps the project organized, reads documentation, tracks progress, prevents scope creep and suggests the next task.

Instructions:

TODO: paste full instructions here.

How to use:

Use this agent every time the project is opened. Ask it to read [AGENTS.md](http://AGENTS.md) and all files in docs/, summarize the project state, and suggest the next unfinished task.

---

## 2. Data Pipeline Agent

Name:

Data Pipeline Agent

Description:

Python data-processing agent focused on loading the Jena Climate dataset, preparing time-series data, selecting the temperature variable, cleaning datetime indexes, and creating artificial missing values for interpolation experiments.

Instructions:

TODO: paste full instructions here.

How to use:

Use this agent for src/data_[loader.py](http://loader.py) and src/[preprocessing.py](http://preprocessing.py).

---

## 3. Interpolation Experiment Agent

Name:

Interpolation Experiment Agent

Description:

Experiment-focused Python agent for implementing classical interpolation methods and machine learning reconstruction models.

Instructions:

TODO: paste full instructions here.

How to use:

Use this agent for src/interpolation_[methods.py](http://methods.py), src/ml_[models.py](http://models.py) and [main.py](http://main.py).

---

## 4. Results Analysis Agent

Name:

Results Analysis Agent

Description:

Evaluation and results analysis agent that calculates MAE, RMSE and R2, creates thesis-ready tables and plots, compares interpolation methods, and writes result notes.

Instructions:

TODO: paste full instructions here.

How to use:

Use this agent for src/[evaluation.py](http://evaluation.py), src/[plots.py](http://plots.py), results/tables/, results/figures/ and docs/results_[notes.md](http://notes.md).

---

## 5. Thesis Writer Agent

Name:

Thesis Writer Agent

Description:

Croatian thesis-writing agent that turns project documentation, methodology, code outputs and result notes into clear formal thesis text.

Instructions:

TODO: paste full instructions here.

How to use:

Use this agent when writing thesis chapters in Croatian.

---

## 6. Code Review Debug Agent

Name:

Code Review Debug Agent

Description:

Defensive Python code review and debugging agent that explains errors, checks for bugs and suggests minimal safe fixes.

Instructions:

TODO: paste full instructions here.

How to use:

Use this agent when python [main.py](http://main.py) fails or when results look wrong.

---

## 7. Literature Review Agent

Name:

Literature Review Agent

Description:

Literature review and citation-support agent for finding, organizing and summarizing sources for the thesis.

Instructions:

TODO: paste full instructions here.

How to use:

Use this agent for literature, citations, related work and theory chapters.