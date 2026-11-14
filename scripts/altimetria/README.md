# Altimetría frente al Perú

Desde la raíz de `data_treatment`, configura una vez la cuenta gratuita con `uv run copernicusmarine login`. Las credenciales se gestionan fuera del repositorio.

```bash
uv run python scripts/altimetria/descargar.py
uv run python scripts/altimetria/analizar.py
```

El NetCDF y su manifiesto se descargan en `/tmp/anchoveta_altimetria/` por defecto. Para conservar los datos entre sesiones, indica un directorio externo al repositorio con `--raw-dir` y pasa el NetCDF con `--input` al segundo comando. Para reemplazar una descarga existente, usa `--force`.

El análisis genera `serie_mensual.csv`, `tendencias.csv`, `comparacion.png` y `proveniencia.json` en `data/tablas_pruebas_pendientes/altimetria/`, además de `docs/pruebas_pendientes/RESULTADOS_ALTIMETRIA.md`. `--output` y `--report` permiten elegir otras rutas; una nueva ejecución reemplaza esas salidas.

El p ajustado corresponde a los 12 contrastes de esta comparación, no a la familia histórica de 162. La conclusión automática usa signo y solapamiento de intervalos individuales como regla descriptiva, no como prueba formal de igualdad. La altimetría no es plenamente independiente de GLORYS, que asimila observaciones altimétricas.
