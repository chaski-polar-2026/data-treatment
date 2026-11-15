# Exportadores recuperados

Copiados de los scripts locales `pruebas/fitoplancton/exportar_ronda_json.py`, `pruebas/fitoplancton/exportar_nino_relaciones.py` y `pruebas/json_pagina/construir_monitor_json.py` el 2026-11-15. Se sustituyeron rutas y se añadió el acceso al módulo común de configuración. No se cambiaron fórmulas, cifras ni textos de resultados. No tienen imports locales adicionales: sus dependencias directas de datos se enumeran en data/inputs/manifest.json.

Todos escriben exclusivamente en data/web_export. El constructor del monitor conserva su fecha de ejecución y sus metadatos originales; no se lo declara idéntico al archivo publicado. `comparar.py --public-data <directorio>` verifica bytes y rutas JSON sin escribir en la web. La copia de base del monitor es una entrada histórica distinta de la versión publicada actual.

El NetCDF ERSST se obtiene por separado según data/inputs/LEEME.md. No hay descarga automática ni credenciales en estos scripts.
