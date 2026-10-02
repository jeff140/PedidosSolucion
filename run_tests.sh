#!/usr/bin/env bash
set -e

echo "=== [1/3] Limpiando artefactos previos de cobertura ==="
rm -rf htmlcov .coverage coverage.xml

echo "=== [2/3] Ejecutando suite de pruebas con pytest-cov ==="
pytest tests/ \
    --cov=src \
    --cov-report=term-missing \
    --cov-report=html:htmlcov \
    --cov-fail-under=85 \
    -v

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "=== [3/3] Pruebas exitosas. Reporte HTML en ./htmlcov/index.html ==="
else
    echo "=== ERROR: Alguna prueba ha fallado o cobertura insuficiente ==="
    exit $EXIT_CODE
fi
