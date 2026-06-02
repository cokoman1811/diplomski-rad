@echo off
cd /d "%~dp0"
echo Running full experiment...
.venv\Scripts\python.exe main.py --run-all --open-report
