# Módulo de Pedidos - Arquitectura Limpia y TDD en Python

Módulo de procesamiento, liquidación y persistencia de pedidos desarrollado bajo la disciplina Test-Driven Development (TDD) y principios de Clean Architecture.

## 1. Justificación Tecnológica
- **Python 3.10+**: Lenguaje de sintaxis limpia y expresiva, con soporte nativo de tipos estáticos (`typing`) y modelos de datos desacoplados mediante `dataclasses`.
- **pytest & pytest-cov**: Framework estándar de pruebas en el ecosistema Python. Brinda manejo eficiente de fixtures, parametrización nativa de casos de prueba y reporte detallado de cobertura de código.
- **FastAPI & HTTPX**: Framework web asíncrono y de alto rendimiento. Permite validación estricta de esquemas con Pydantic y pruebas de integración inmediatas con `TestClient` sin necesidad de levantar sockets de red reales.

---

## 2. Instalación y Ejecución

### Requisitos previos
- Python 3.10 o superior instalado.

### Configuración del entorno virtual
```powershell
# En la raíz de PedidosSolution:
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt