# Reproducir los análisis existentes

## Entorno

No se descarga ni instala nada al ejecutar el runner. `pyproject.toml` declara Python >=3.14 para el proyecto completo. Esta verificación pudo ejecutar los scripts independientes con el intérprete disponible Python 3.12.10 y numpy 2.5.2, pandas 3.1.0, scipy 1.18.1, xarray 2026.9.0, netCDF4 1.7.5.1.post1. La instalación completa del proyecto en Python 3.14 queda pendiente; no se cambió su requisito. Se añadió numpy a las dependencias directas; las otras cuatro ya figuraban. No se actualizó el entorno ni el lockfile.

## Entradas

Consultar [inventario y hashes](../data/inputs/LEEME.md). La variable opcional `CHASKI_DATA` cambia únicamente la raíz de entradas; por defecto `data/inputs/`. Las dos copias del monitor son idénticas, y el snapshot usado procede del repositorio. No se carga configuración secreta. Los cinco análisis de la ejecución conjunta no necesitan red ni ERSST. Los históricos adicionales pueden necesitar entradas no incluidas, que deben declararse antes de ejecutarlos.

## Una ejecución

Desde PowerShell, en cualquier carpeta (usar la ruta al script si no se está en la raíz):

```powershell
$env:PYTHONIOENCODING = 'utf-8'
python scripts/reproducir_pruebas.py --rapido
```

Sin `--rapido`, bloque 5 usa los 2000 sustitutos originales. Con `--rapido`, usa 100: **prueba de infraestructura, no resultado equivalente al preregistro**. Las funciones y criterios no se cambian; no se añaden hipótesis. Orden: bloques 1, 3, 4, 5 y Antártida–Chile/Argentina. `--bloques 1,3,4` limita la verificación a los bloques solicitados en A6. Nunca usar `-I`, porque los módulos locales deben poder importarse.

Cada proceso guarda su log bajo `data/reproducciones/`. Tablas en `data/reproducciones/data/tablas_pruebas_pendientes/`, JSON de perspectiva en `data/reproducciones/data/` e informe reproducido del bloque 5 en `data/reproducciones/docs/pruebas_pendientes/`. Los resultados confirmados no se sobrescriben, incluso al ejecutar directamente los scripts actualizados. Los scripts de descarga conservan sus opciones habituales y no forman parte del runner.

`comparacion.json` compara con `git show HEAD:ruta`; en una copia limpia sin `.git`, compara con los archivos de referencia copiados del repositorio. IDENTICAL significa igualdad de bytes; LINE_ENDINGS_ONLY significa igualdad tras normalizar CRLF/LF; DIFFERENT conserva ambos archivos y devuelve error; RAPIDO_NOT_EQUIVALENT identifica tablas alteradas por reducir sustitutos. METADATA_PATHS_ONLY identifica nombres de rutas distintos con los mismos hashes de entradas. Se guardan los logs aunque un bloque falle.

## Resultados esperados y verificación realizada

- Bloque 1: 896 pruebas; 0 con q parcial <0,05.
- Bloque 3: 90 combinaciones; la tabla y perspectiva_acierto.json coinciden con Git. Esto reproduce el análisis histórico, sin reinterpretar su conclusión.
- Bloque 4: tabla de 16 filas; coincide con Git. Se conservan los resultados originales.
- Bloque 5: 1200 pruebas, 0 con q parcial <0,05; modo rápido no valida p empíricos finales. La reproducción completa con 2000 sustituye solo salidas aisladas.
- Vecinos: tabla de 48 filas; coincide con Git. La pista de sardina araucana no se promueve a hallazgo, según el informe histórico.

La ejecución en el árbol de trabajo coincidió numéricamente en bloques 1/3/4 y vecinos, con diferencias exclusivamente de finales de línea. Una copia temporal limpia, sin archivos personales ni variables externas, ejecutada desde una carpeta ajena, devolvió 0: bloques 1/3/4, vecinos y perspectiva fueron idénticos byte a byte; bloque 5 rápido mostró las diferencias esperadas. Ver [informe de verificación](reproducibilidad/VERIFICACION.md).

## Exportar los datos de la web

```powershell
python scripts/web_export/construir_monitor_json.py
python scripts/web_export/exportar_nino_relaciones.py
python scripts/web_export/exportar_ronda_json.py
```

Salidas aisladas: `data/web_export/`. El último requiere ERSST separado; falta => mensaje claro con ruta y referencia al inventario. No hay descargas automáticas. La carpeta temporal de prueba aportó el ERSST histórico y no se incorporó a Git. Ronda y Niño son idénticos a los publicados. **Monitor no es idéntico**: 198 rutas JSON difieren, principalmente datos de 2026 y metadatos; no se publicó ni reemplazó la web. No se debe atribuir la diferencia únicamente a generated_at. Auditoría estructural completa en `docs/reproducibilidad/comparacion_web.json`. El constructor original conserva fecha de ejecución dinámica, por lo que no promete identidad de bytes entre ejecuciones; la comparación debe revisar también datos y metadatos.

Si se solicita igualdad total del monitor, el equipo debe resolver qué entrada/versión de 2026 y qué metadatos son autoritativos antes de modificar su cálculo o publicar. La configuración de rutas no corrige discrepancias científicas ni reemplaza resultados.

Para repetir la comparación web sin escribir en su directorio: `python scripts/web_export/comparar.py --public-data <carpeta-public/assets/data>`. Devuelve 1 si hay diferencias y guarda la auditoría en data/web_export/comparacion_web.json. El runner valida primero todos los SHA-256 del manifiesto.

Verificación adicional: bloque 5 completo, 2000 sustitutos, siete CSV idénticos byte a byte; metadatos difieren solo en las rutas de entradas, con hashes iguales.

`.gitattributes` desactiva la conversi?n de finales de l?nea para data/inputs: los hashes del manifiesto corresponden tambi?n a los blobs confirmados en Git, independientemente de core.autocrlf. No se aplic? esta regla a tablas hist?ricas ni a especies.
