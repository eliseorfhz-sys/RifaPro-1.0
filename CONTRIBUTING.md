# Guía de contribución

Gracias por colaborar con **RifaPro-1.0**.

## Flujo recomendado

1. Haz un fork o trabaja en una rama nueva:
   - `feature/nombre-cambio`
   - `fix/descripcion-corta`
2. Mantén los cambios enfocados y pequeños.
3. Abre Pull Request con descripción clara de:
   - problema que resuelve
   - alcance del cambio
   - pasos para validarlo

## Convención de commits (sugerida)

Formato:

`tipo(scope): mensaje corto`

Tipos comunes:

- `feat`: nueva funcionalidad
- `fix`: corrección de errores
- `docs`: cambios de documentación
- `refactor`: mejora interna sin cambiar comportamiento esperado
- `test`: pruebas
- `chore`: tareas de mantenimiento

## Validación local

Antes de abrir PR:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Verifica manualmente la herramienta afectada (nombres, comentarios, ruleta o números).

## Estilo de código

- Mantén la interfaz en español.
- Reutiliza funciones existentes (`parse_lines`, `apply_filters`, `reveal_winners_one_by_one`, etc.).
- Evita cambios cosméticos no relacionados con el objetivo del PR.

## Reportes y mejoras

- Bugs: describe pasos para reproducir y resultado esperado vs. actual.
- Features: explica el caso de uso y el beneficio para el usuario final.
