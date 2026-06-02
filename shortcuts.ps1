# Thesis project shortcuts (PowerShell)
#
# IMPORTANT: load this file BEFORE using run / runfast:
#   . .\shortcuts.ps1
#
# Alternative (no loading needed):
#   .\runfast.bat
#   .\run.bat
#
# Commands after loading:
#   runpy    - activate .venv
#   pyoff    - deactivate .venv
#   run      - full experiment (python main.py --run-all)
#   runfast  - quick experiment (python main.py --quick)

$script:ThesisRoot = $PSScriptRoot
$script:ThesisPython = Join-Path $ThesisRoot ".venv\Scripts\python.exe"

function runpy {
    if (Test-Path ".\.venv\Scripts\Activate.ps1") {
        . .\.venv\Scripts\Activate.ps1
        Write-Host "Virtual environment activated." -ForegroundColor Green
    }
    else {
        Write-Host "No .venv found in this folder." -ForegroundColor Red
    }
}

function pyoff {
    deactivate
}

function _Invoke-ThesisPython {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Arguments
    )

    if (-not (Test-Path $script:ThesisPython)) {
        Write-Host "Python not found: $script:ThesisPython" -ForegroundColor Red
        Write-Host "Create the venv first, then install requirements." -ForegroundColor Yellow
        return
    }

    Push-Location $script:ThesisRoot
    try {
        & $script:ThesisPython @Arguments
    }
    finally {
        Pop-Location
    }
}

function run {
    <#
    .SYNOPSIS
    Runs the full thesis experiment on the complete Jena dataset.
    #>
    Write-Host "Running full experiment: python main.py --run-all" -ForegroundColor Cyan
    _Invoke-ThesisPython -Arguments @("main.py", "--run-all")
}

function runfast {
    <#
    .SYNOPSIS
    Runs a quick experiment on a smaller data slice for testing.
    #>
    Write-Host "Running quick experiment: python main.py --quick" -ForegroundColor Cyan
    _Invoke-ThesisPython -Arguments @("main.py", "--quick")
}

Write-Host "Thesis shortcuts loaded: run, runfast, runpy, pyoff" -ForegroundColor Green
