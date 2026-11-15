# data-treatment

Descarga, preparación y análisis de datos ambientales y pesqueros para estudiar
asociaciones entre variables del océano Austral, el sistema de la Corriente de
Humboldt y la anchoveta peruana (*Engraulis ringens*).

Los resultados son **asociaciones exploratorias**, no pruebas de causalidad ni
de transporte físico entre la Antártida y el Perú.

## Estructura

| Carpeta | Contenido |
|---|---|
| `src/nasahackaton/` | Paquete Python: fuentes, descargas, transformaciones y modelos |
| `scripts/` | Scripts numerados del pipeline (descarga → paneles → experimentos) |
| `analysis_r/` | Pipeline estadístico en R (contraste H0/H1); ver `analysis_r/README.md` |
| `data/` | Datos versionados pequeños; `data/punto1_anchoveta/` tiene desembarques, cuotas y biomasa con un `LEEME.md` por fuente |
| `docs/` | Metodología, reportes e informe del análisis exploratorio |

## Instalación

Python (requiere [uv](https://docs.astral.sh/uv/); instala Python 3.14 si falta):

```bash
uv sync
uv run python scripts/<script>.py
```

R (4.x, solo para `analysis_r/`):

```bash
Rscript analysis_r/00_install_packages.R
```

## Reproducir el análisis exploratorio

`data/processed/` no se versiona, así que los paneles intermedios deben
regenerarse con los scripts de `scripts/`. Para repetir solo los modelos con el
panel ya usado en el informe:

```bash
Rscript analysis_r/04_exploratory_models.R \
  --panel analysis_r/data/exploratory_nointerp/exploratory_cruise_panel_used.csv \
  --out-dir <carpeta_de_salida>
```

## Fuentes

Cada conjunto de datos indica su fuente en su `LEEME.md` o en
`docs/01_metodologia/metodologia.md`. Fuentes principales: IMARPE (cruceros y biomasa), BCRP
(desembarques), PRODUCE (cuotas y temporadas), RAM Legacy v4.44, NOAA PSL/CPC
(Niño 1+2, PDO, AAO/SAM), NSIDC (hielo marino antártico), ESA OC-CCI
(clorofila), Copernicus Marine y World Ocean Atlas 2023.

## Limitaciones

Ver `docs/04_analisis/informe_analisis_exploratorio_h1_h0.md` (sección 4.4). En resumen:
pocos cruceros con fechas completas, resultados sensibles a la estructura
temporal y respuestas biológicas que no deben combinarse entre sí.

Alcance de las variables:

- **Niño 1+2, temperatura y clorofila** son el núcleo del análisis y alimentan el monitor y el juego del repositorio `chaski-polar-webpage`.
- **Carbono fitoplanctónico** entra solo como una respuesta exploratoria (`ab_phytoplankton_carbon`) y no se mezcla con la clorofila.
- **Temperatura y oxígeno a 100–200 m** tienen una ronda de tendencias en `docs/pruebas_pendientes/RESULTADOS_RONDA_SEIS_VARIABLES.md`; todavía no se usan en el monitor ni en el juego.
- **Licencia:** el repositorio aún no tiene archivo de licencia; el equipo debe elegirla antes de la entrega (Space Apps pide contenido original open source).


## Estructura del repositorio

- `src/nasahackaton/`: código del proyecto y monitor de referencia.
- `scripts/`: descarga y procesamiento; `scripts/web_export/` contiene los exportadores recuperados.
- `docs/pruebas_pendientes/`: preregistros, scripts y resultados históricos.
- `data/inputs/`: snapshots pequeños, procedencia y SHA-256 para reproducir sin red.
- `data/tablas_pruebas_pendientes/`: tablas confirmadas; no se sobrescriben al reproducir.
- `data/reproducciones/` y `data/web_export/`: salidas locales ignoradas por Git.

## Cómo reproducir

Consultar [docs/REPRODUCIR.md](docs/REPRODUCIR.md). El comando `python scripts/reproducir_pruebas.py --rapido`, con PYTHONIOENCODING=utf-8 y sin -I, verifica la infraestructura sin tocar resultados históricos. El modo completo mantiene los 2000 sustitutos del bloque 5. Entradas configurables mediante CHASKI_DATA.

## Resumen de resultados documentados

- Bloque 1: ninguna de las 896 pruebas pasa FDR; perspectiva retrospectiva y desembarques se describen en [su informe](docs/pruebas_pendientes/RESULTADOS_TELECONEXION_Y_PERSPECTIVA.md).
- Nutrientes a largo plazo: ninguna de las 1200 pruebas cumple el criterio preregistrado; un nulo con este registro no demuestra ausencia de vínculo lento. [Informe](docs/pruebas_pendientes/RESULTADOS_NUTRIENTES_LARGO_PLAZO.md).
- Antártida y vecinos: las pistas no se presentan como hallazgos confirmados. [Informe](docs/pruebas_pendientes/RESULTADOS_ANTARTIDA_VECINOS.md).
- Altimetría y GLORYS coinciden parcialmente; dependencia y correcciones limitan la comparación. [Informe y nota](docs/pruebas_pendientes/RESULTADOS_ALTIMETRIA.md).

## Datos para la web

Los scripts de `scripts/web_export/` escriben en `data/web_export/`; no escriben en el repositorio web. La verificación reproduce exactamente tendencias-ronda.json y nino-relaciones.json; monitor-data.js presenta diferencias de 2026/metadatos que deben resolverse antes de publicar. Fuentes en [el catálogo](docs/02_datos/FUENTES_DE_DATOS.md); licencia pendiente de [decisión del equipo](docs/LICENCIA_PENDIENTE.md).
