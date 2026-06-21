# Política de seguridad

Gracias por ayudar a mantener **RifaPro-1.0** seguro.

## Versiones soportadas

Actualmente se brinda soporte de seguridad a la rama principal activa del proyecto.

## Cómo reportar una vulnerabilidad

Si encuentras una posible vulnerabilidad:

1. **No** abras un issue público con detalles explotables.
2. Reporta de forma privada al mantenedor del repositorio.
3. Incluye:
   - descripción del problema,
   - impacto potencial,
   - pasos para reproducir,
   - propuesta de mitigación (si aplica).

## Proceso de respuesta (objetivo)

- Confirmación de recepción inicial: dentro de 72 horas.
- Evaluación y priorización: según severidad e impacto.
- Comunicación de estado: periódica hasta resolución.
- Publicación responsable: al liberar el fix.

## Buenas prácticas del proyecto

- No subir secretos ni tokens en `.streamlit/secrets.toml`.
- Validar entradas de usuario en nuevas funcionalidades que procesen datos externos.
