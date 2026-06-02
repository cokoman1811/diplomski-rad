# Style guide

## Purpose

This file defines the style rules for code, plots, documentation and thesis writing in this project.

The goal is to keep the project simple, readable and suitable for a master's thesis.

---

## Code style

All code should be written in a clear and simple way.

Rules:

- Use Python.
- Use English for code, variable names, function names and comments.
- Use clear and descriptive names.
- Keep functions small.
- Avoid unnecessary abstraction.
- Avoid complicated code if a simple solution is enough.
- Add short docstrings to important functions.
- Add comments only when they help explain the logic.
- Do not over-engineer the project.
- Do not add unnecessary frameworks.

Good examples:

```python
def load_temperature_series(file_path):
    """Load temperature data as a pandas Series with datetime index."""