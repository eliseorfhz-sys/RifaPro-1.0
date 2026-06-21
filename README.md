# RifaPro-1.0

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](#requisitos)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)](#ejecución)
[![Licencia](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)
[![Estado](https://img.shields.io/badge/Estado-En%20desarrollo-orange.svg)](#roadmap)

Aplicación web local en **Streamlit** para crear sorteos justos y transparentes.
Inspirada en [AppSorteos](https://app-sorteos.com/es/app), funciona sin registro y genera certificados de transparencia en cada resultado.

## Características principales

- **Ganador aleatorio:** elige uno o varios ganadores a partir de una lista de nombres.
- **Sorteo de comentarios:** filtra comentarios por hashtag, menciones, duplicados y usuarios bloqueados.
- **Ruleta de la fortuna:** ruleta animada con eliminación automática de ganadores previos.
- **Números aleatorios:** genera secuencias numéricas con o sin repetición.
- Animación giratoria opcional al revelar ganadores.
- Certificado de sorteo con fecha, participantes y algoritmo utilizado.
- Interfaz en español, lista para usar en eventos, rifas y redes sociales.

## Requisitos

- Python 3.10+ (recomendado)
- Dependencias en `requirements.txt`

## Instalación

1. Clona este repositorio:

```bash
git clone https://github.com/eliseorfhz-sys/RifaPro-1.0.git
cd RifaPro-1.0
```

2. (Opcional, recomendado) Crea y activa un entorno virtual:

```bash
python -m venv .venv
```

En Windows (PowerShell):

```bash
.venv\Scripts\Activate.ps1
```

3. Instala dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
streamlit run app.py
```

La aplicación se abrirá en tu navegador (por ejemplo `http://localhost:8501`).

## Uso rápido

1. Elige una herramienta en la barra lateral.
2. Ingresa participantes (nombres, comentarios, opciones o rango numérico).
3. Configura filtros o número de ganadores si lo necesitas.
4. Pulsa el botón de sorteo y revisa el certificado de transparencia.

## Estructura mínima del proyecto

- `app.py`: aplicación principal de Streamlit.
- `wheel_component.py`: componente HTML de la ruleta animada.
- `requirements.txt`: dependencias.
- `.github/`: CI y plantillas de issues/PR.
- `.gitignore`: exclusiones para desarrollo.

## Roadmap

- [ ] Exportar certificados de sorteo a PDF o imagen.
- [ ] Guardar historial local de sorteos realizados.
- [ ] Importar participantes desde CSV o Excel.
- [ ] Modo pantalla completa para proyección en eventos.
- [ ] Pruebas automáticas básicas de regresión.

## Contribuir

Las contribuciones son bienvenidas. Revisa primero [`CONTRIBUTING.md`](./CONTRIBUTING.md) para conocer
el flujo propuesto (ramas, formato de commits, validaciones y estilo).

## Historial de cambios

Consulta [`CHANGELOG.md`](./CHANGELOG.md) para ver las versiones y cambios relevantes del proyecto.

## Seguridad

Consulta [`SECURITY.md`](./SECURITY.md) para el proceso de reporte de vulnerabilidades.

## Autor

- **Eliseo Refugio Hernandez**
- Lista de contributors: [`CONTRIBUTORS.md`](./CONTRIBUTORS.md)

## Licencia

Este proyecto se distribuye bajo licencia MIT. Revisa el archivo [`LICENSE`](./LICENSE).
