# Estado de datos: conexión Océano Austral–Humboldt–anchoveta

**Fecha de revisión:** 15 de noviembre de 2026  
**Propósito:** dejar claro qué datos hacen falta para probar una conexión subsuperficial de nutrientes y cómo obtener lo que ya está cubierto por el pipeline.

## Resumen

El repositorio ya contiene un pipeline reproducible para descargar campos regionales de Copernicus Marine en seis cajas desde la Península Antártica hasta el mar peruano. El código está en `scripts/07_download_connectivity.py`; construye tres NetCDF por región con temperatura, salinidad, corrientes, altura del mar, capa de mezcla, nitrato, fosfato, oxígeno, clorofila y carbono fitoplanctónico.

En esta copia de trabajo no están los NetCDF regionales bajo `data/raw/connectivity/`. Ese directorio y otros archivos crudos están excluidos del control de versiones por `.gitignore`. El panel estadístico descrito en reportes previos proviene de una ejecución anterior, pero sus archivos fuente no están presentes aquí. Por tanto, las descargas deben regenerarse antes de reproducir el análisis.

## Inventario de datos requeridos

| Eslabón | Datos | Estado en esta copia | Fuente o ruta |
|---|---|---|---|
| Fuente austral y ruta del Pacífico Sur | Temperatura, salinidad y corrientes 3D (`thetao`, `so`, `uo`, `vo`) hasta 1000 m | Descargador disponible; NetCDF ausentes | Copernicus Marine, `scripts/07_download_connectivity.py` |
| Nutrientes y respuesta biogeoquímica | Nitrato, fosfato y oxígeno 3D hasta 500 m; clorofila y carbono | Descargador disponible; NetCDF ausentes | Copernicus Marine, `scripts/07_download_connectivity.py` |
| Forzamiento costero peruano | Viento zonal y meridional ERA5 | Hay un NetCDF mensual en `data/raw/era5/wind_monthly.nc`, pero el descargador actual lo recorta al dominio peruano; verificar sus fechas/cobertura antes de integrar | ERA5/CDS; `scripts/02_download_experiment_b.py` |
| Hielo antártico | Extensión agregada diaria | Disponible; no identifica sectores ni una ruta de masas de agua | NSIDC G02135, `data/raw/nsidc/S_seaice_extent_daily_v4.0.csv` |
| Hielo espacial | Concentración en grilla polar | Descarga prevista en el pipeline; no validada en esta copia | NSIDC G02202, `scripts/08_download_sea_ice.py` |
| Corrientes superficiales independientes | Velocidad superficial OSCAR | Descargador disponible; cobertura local no validada aquí | NASA PO.DAAC, `scripts/09_download_oscar.py` |
| Perfiles observacionales subsuperficiales | Temperatura/salinidad y, si están disponibles, nitrato/oxígeno/clorofila | No se encontraron perfiles Argo/BGC-Argo guardados en esta copia | Argo GDAC; BGC-Argo mide variables biogeoquímicas en algunos flotadores |
| Respuesta de anchoveta | Biomasa acústica, NASC por transecto, fecha y posición | Hay resúmenes de biomasa por crucero, pero no NASC georreferenciado ni cobertura armonizada en esta copia | IMARPE; los informes de crucero deben vincularse con sus datos acústicos originales |

## Descarga regional ya implementada

El pipeline de Copernicus utiliza estas seis regiones: Península Antártica, Bellingshausen, Pacífico Sur intermedio, Pacífico Sur subtropical, transición hacia Humboldt y Humboldt peruano. Mantiene los NetCDF por región y separa la física de la biogeoquímica.

Desde la raíz del repositorio, cuando Python y las dependencias estén instalados y la cuenta Copernicus esté configurada:

```powershell
py -m venv .venv
.venv\Scripts\python.exe -m pip install -e .
.venv\Scripts\copernicusmarine.exe login
.venv\Scripts\python.exe scripts/07_download_connectivity.py --start 1993-01-01 --end 2025-12-01 --physics-max-depth 1000 --bgc-max-depth 500
.venv\Scripts\python.exe scripts/12_validate_connectivity.py
.venv\Scripts\python.exe scripts/11_build_connectivity_panel.py
```

El periodo inicial del panel peruano del proyecto es 1998–2025. Extender la descarga física a 1993 permite aprovechar el inicio del reanálisis global; se debe comprobar el solapamiento real de cada variable y producto, y usar el periodo común al ajustar el modelo. Los productos son reanálisis, no observaciones independientes.

## Datos que el pipeline no obtiene todavía

1. **Trazadores de origen de masas de agua.** Los campos de temperatura, salinidad y corriente permiten caracterizar masas de agua, pero una asociación no demuestra que una parcela de agua o nutriente viajó desde la Antártida hasta Perú. Una prueba de ruta requeriría trayectorias lagrangianas o trazadores etiquetados y validación con perfiles observados.
2. **Perfiles Argo/BGC-Argo emparejados con la ruta.** Incorporar perfiles de temperatura y salinidad; nitrato, oxígeno, clorofila o irradiancia solo cuando el flotador realmente mida esas variables. Guardar identificador del flotador, fecha, posición, profundidad, bandera de calidad y sensor.
3. **Afloramiento local calculado de forma explícita.** Derivar el transporte de Ekman costero con el estrés del viento y añadir nitrato en la profundidad fuente. No sustituir el afloramiento por una corriente superficial o por la clorofila.
4. **Biomasa acústica con soporte espacial.** Solicitar/recuperar de IMARPE fechas exactas, transectos, coordenadas, NASC por especie, estrato de profundidad, stock y método de conversión a biomasa. Los desembarques no sustituyen esa respuesta biológica.

## Criterio de análisis

Emparejar primero anomalías mensuales de agua subsuperficial y nutrientes por región; después contrastarlas con el índice local de afloramiento y nutrientes de la costa peruana. Controlar estacionalidad, ENSO, SAM, viento local, luz y oxígeno. Mantener una ventana de rezagos predefinida, corregir por pruebas múltiples y validar fuera de muestra cuando el número de observaciones biológicas lo permita.

No informar un “porcentaje de nutrientes antárticos” como resultado peruano sin un balance de masas o trazador validado. El reanálisis por sí solo permite asociaciones y consistencia física, no una atribución causal de origen.

## Referencias de datos

- Copernicus Marine, reanálisis físico global: <https://data.marine.copernicus.eu/product/GLOBAL_MULTIYEAR_PHY_001_030>
- Copernicus Marine, documentación del reanálisis biogeoquímico global: <https://documentation.marine.copernicus.eu/QUID/CMEMS-GLO-QUID-001-029.pdf>
- Argo GDAC, acceso a perfiles: <https://argo.ucsd.edu/data/data-from-gdacs/>
- Variables aprobadas de BGC-Argo: <https://argo.ucsd.edu/about/framework-for-entering-argo/guidelines-for-argo-floats/>
- IMARPE, colección de campañas hidroacústicas y recursos pelágicos: <https://repositorio.imarpe.gob.pe/>

## Pruebas ya realizadas con los datos locales (15/11/2026)

Con el panel de conectividad que ya existe (reanálisis Copernicus, 1998-2025) se corrieron pruebas preregistradas, con tamaño efectivo por autocorrelación, corrección FDR, control de El Niño y comprobación sin años extremos y por mitades. Los resultados completos están en `docs/pruebas_pendientes/`:

1. **Señales antárticas y del Pacífico sur frente a la costa peruana** (896 pruebas, retrasos de 0 a 12 meses): ninguna supera el FDR, ni en correlación cruda ni controlando El Niño. Ver `RESULTADOS_TELECONEXION_Y_PERSPECTIVA.md`, bloque 1.
2. **Nutrientes, oxígeno y masas de agua a 200-500 m con retrasos de hasta 5 años** (1200 pruebas): ninguna supera el FDR (menor q = 0,053); tamaño efectivo mediano de unos 14 datos, con baja potencia. No se detecta vínculo con estos datos, lo que no prueba que no exista un vínculo lento. Ver `RESULTADOS_NUTRIENTES_LARGO_PLAZO.md` y su preregistro.
3. **Antártida y capturas de Chile y Argentina** (48 pruebas): las pistas anteriores de jurel y calamar no se sostienen con el método estricto. Ver `RESULTADOS_ANTARTIDA_VECINOS.md`.
4. **Perspectiva retrospectiva a 1 a 3 meses**: la temperatura del mar mejora a la climatología en las cinco zonas; la clorofila solo a 1 mes. El Niño no mejora la predicción mensual de los desembarques de anchoveta. Ver el mismo informe del punto 1 y `data/perspectiva_acierto.json`.
5. **Índices PSA y del Mar de Amundsen**: no existen en disco; el script `prueba_indices_externos.py` queda listo para cuando se consigan.

Lo que sigue faltando para una prueba más fuerte es lo que enumera este documento: trazadores de masas de agua, afloramiento calculado de forma explícita, perfiles Argo y BGC-Argo y biomasa acústica con soporte espacial.

