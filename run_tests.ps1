$ErrorActionPreference = "Stop"

Write-Host "=== [1/3] Limpiando reportes previos de cobertura ===" -ForegroundColor Cyan
if (Test-Path htmlcov) { Remove-Item -Recurse -Force htmlcov }
if (Test-Path .coverage) { Remove-Item -Force .coverage }

Write-Host "=== [2/3] Ejecutando pruebas unitarias e integracion ===" -ForegroundColor Cyan
pytest tests/ `
    --cov=src `
    --cov-report=term-missing `
    --cov-report=html:htmlcov `
    --cov-fail-under=85 `
    -v

if ($LASTEXITCODE -eq 0) {
    Write-Host "=== [3/3] Pruebas completadas. Reporte HTML en ./htmlcov/index.html ===" -ForegroundColor Green
} else {
    Write-Host "=== ERROR: Se encontraron fallos en la ejecucion ===" -ForegroundColor Red
    exit 1
}
