@echo off
cd /d "%~dp0"
echo Running quick experiment...
.venv\Scripts\python.exe main.py --quick --open-report
if errorlevel 1 (
  echo.
  echo Run failed. Use: .venv\Scripts\python.exe main.py --quick --open-report
  pause
)