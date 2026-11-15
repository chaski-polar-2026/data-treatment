# Verificación de reproducibilidad y pendientes

Fecha de comprobación: 2026-11-15. No se ejecutaron análisis nuevos; solo scripts existentes con cambios de rutas/salidas y opción rápida explícita.

## Reproducción

Los bloques 1, 3 y 4 y el análisis de vecinos corren con entradas relativas. No hubo diferencias numéricas contra Git; en el árbol de trabajo cambian solamente CRLF/LF. En la copia temporal limpia, ejecutada desde fuera de la raíz y sin CHASKI_DATA, sus CSV y el JSON de perspectiva son idénticos byte a byte. Todos los procesos devolvieron 0. Bloque 5 rápido ejecutó 100 sustitutos y produjo diferencias esperadas: no equivale al análisis preregistrado de 2000. Ninguna tabla confirmada se sobrescribió.

El exportador de ronda falló inicialmente por ausencia de ERSST, con FileNotFoundError y mensaje explícito. Al aportar el archivo histórico en una carpeta temporal, terminó con retorno 0 y coincidió con la web. El constructor de monitor y exportador Niño devolvieron 0. Ronda y Niño idénticos byte a byte; monitor difiere en 198 rutas JSON, no solo en generated_at. La auditoría lista los campos de 2026 y metadatos. No se editó la web.

La declaración Python >=3.14 del proyecto completo no se pudo verificar: el intérprete disponible es 3.12.10. Los scripts independientes y sus dependencias instaladas sí se ejecutaron. No se instaló ni actualizó ningún paquete ni se cambió uv.lock. La dependencia directa numpy fue añadida al pyproject.

## C1: comprobación al azar de especies, solo documentación

Muestra de tres de los cinco valores nuevos citados F24/F25, sin reemplazo, semilla 20261115. Los enlaces F24 (estudio de cachema, sección Cynoscion analis / Figura 6) y F25 (guía IMARPE, p. 49) se abrieron sin sesión, pero devolvieron HTTP 502 en esta comprobación. **0 confirmados de nuevo, 3 no verificables por acceso; 0 contradicciones demostradas.** No se usan verificaciones antiguas para afirmar acceso actual. Las tablas y JSON de especies permanecen intactos.

- merluza.depth_min_m = 50; F25, p. 49; habitat; estado: **no accesible (HTTP 502)**.
- cachema.depth_min_m = 0; F24, Section Cynoscion analis; Figure 6; estado: **no accesible (HTTP 502)**.
- cachema.depth_max_m = 50; F24, Section Cynoscion analis; Figure 6; estado: **no accesible (HTTP 502)**.

Fuentes: https://repositorio.imarpe.gob.pe/server/api/core/bitstreams/e4be9243-04b5-4ad6-8e84-a8b992245a66/content y https://repositorio.imarpe.gob.pe/server/api/core/bitstreams/28ef125d-e7d8-4594-8584-64609ca389c4/content . Reintentar manualmente cuando el servicio esté disponible; no se eludieron bloqueos.

## C2: cifras de literatura

Se abrieron los textos completos Jones 2016, Kadko 2017, Hauschildt 2021 y Doering 2019. Resultado detallado fuera del repositorio: VERIFICACION_CIFRAS.md en la carpeta de guías. Jones confirma el porcentaje en un experimento de trazadores modelados, no transporte observado hacia Perú. Kadko contiene ambos números pero no un intervalo homogéneo. La cifra del filamento estaba mal contextualizada: el texto distingue agua subsuperficial y capa mezclada del filamento. No se cambió la web.

## Protección y limpieza

El equipo autorizó sustituir únicamente rutas personales en documentos históricos. Se conservaron cifras, métodos y conclusiones; la nota nueva de comparabilidad en RESULTADOS_ALTIMETRIA.md es la excepción documental solicitada. No se cambió data/especies ni tablas de resultados. Sin archivos LICENSE ni credenciales. El NetCDF de 162 MB no se añadió al repositorio.


También se reprodujo el bloque 5 completo con 2000 sustitutos: sus siete CSV fueron idénticos byte a byte. En metadatos cambian solo las claves de rutas; los hashes de entradas son los mismos (METADATA_PATHS_ONLY). El informe histórico no se sobrescribió. El comando comparador web devuelve 1, correctamente, por las 198 diferencias del monitor; esto no es un error de ejecución ni se ignora.

La versi?n final del runner con comprobaci?n previa de SHA-256 tambi?n se ejecut? desde copia limpia con --rapido: retorno 0 (comparacion_limpia.json). Se verificaron adem?s todos los hashes de los blobs de entrada confirmados en Git, tras desactivar su conversi?n de saltos de l?nea. El barrido de rutas personales en scripts y docs no devuelve coincidencias.
