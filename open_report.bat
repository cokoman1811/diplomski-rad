@echo off
cd /d "%~dp0"
if not exist "results\report.html" (
  echo Report not found. Run runfast.bat or run.bat first.
  pause
  exit /b 1
)
start "" "%~dp0results\report.html"
