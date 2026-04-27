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