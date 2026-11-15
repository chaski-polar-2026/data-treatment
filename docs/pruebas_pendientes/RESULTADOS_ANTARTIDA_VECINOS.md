# Antártida y países vecinos (Chile y Argentina): capturas frente a señales antárticas

Fecha: 14/11/2026. Script: `antartida_vecinos.py`. Tabla completa: `data/tablas_pruebas_pendientes/antartida_vecinos.csv` (48 pruebas).

## Pregunta
¿Las señales antárticas (hielo marino, índice SAM, clorofila de Rey Jorge) se asocian con las capturas anuales de Chile y Argentina?

## Método
- Pares fijados de antemano: Chile (jurel, anchoveta, sardina común, sardina araucana, merluza del Pacífico sur, pota) y Argentina (calamar argentino, merluza argentina), frente a tres señales y dos desfases (0 y 1 año). Total: 48 pruebas.
- Periodo 1998-2024 (n = 27, o 26 con desfase). Capturas FAO (solo pesca), en logaritmo.
- Se calcula la correlación de los **cambios de un año al siguiente** (primeras diferencias), para quitar tendencias y movimientos lentos compartidos. También se informan los niveles, la correlación tras quitar la tendencia lineal a ambas series y la correlación parcial controlando el Niño 1+2.
- El p usa un tamaño de muestra efectivo que considera la autocorrelación. Corrección por pruebas múltiples (FDR de Benjamini-Hochberg) sobre las 48 pruebas.
- Las capturas no miden la abundancia: las afectan cuotas, esfuerzo y colapsos por sobrepesca.

## Resultados
- 3 de 48 pruebas tienen p < 0,05 en diferencias (por azar se esperarían unas 2,4) y 1 supera el FDR al 5 %.
- **Sardina araucana (Chile) frente a la clorofila de Rey Jorge (diciembre a marzo) del año anterior:** r = −0,74 en diferencias, p = 0,001, q = 0,037. Resiste quitar un año cualquiera (r entre −0,68 y −0,79) y la correlación por rangos (−0,64). **No se considera un hallazgo:** no hay un mecanismo plausible, las capturas dependen de cuotas y hubo un colapso en 2013, y surge de mirar muchas combinaciones. Solo se sostendría si se repite con una serie independiente (por ejemplo, evaluaciones de stock).
- **Jurel de Chile frente al hielo marino:** r en diferencias = −0,02 (desfase 0) y −0,09 (desfase 1). Tras quitar la tendencia a ambas series, r = −0,60 pero con p = 0,14 al considerar la autocorrelación. No es significativa.
- **Calamar argentino frente a la clorofila de Rey Jorge del año anterior:** r en diferencias = +0,41 (p = 0,055, q = 0,42); sin tendencia, r = +0,45 (p = 0,017 sin corregir). No supera el FDR.

## Por qué cambian las pistas anteriores
El análisis previo (`datos/pesquerias/analisis3.py`) quitó la tendencia solo a las capturas, dejó la señal antártica con su tendencia y su variación lenta, y calculó el p sin considerar la autocorrelación. Con ese método el hielo y el jurel daban r ≈ −0,55 y la clorofila de Rey Jorge y el calamar r = +0,60. Al tratar ambas series igual y ajustar la autocorrelación, esas relaciones no se sostienen.

## Conclusión
No hay evidencia sólida de que la Antártida afecte las capturas de Chile y Argentina en estos datos. Las "pistas moderadas" de jurel y calamar quedan descartadas. La única asociación que pasa el FDR (sardina araucana) es exploratoria y sin mecanismo conocido.

## Límites
- 27 años anuales dan poca potencia.
- No se probaron efectos directos en el clima de Chile y Argentina (por ejemplo, SAM sobre lluvia y temperatura): no hay datos de esos países en el proyecto.
- Las capturas no son abundancia.

## Reproducir
Las rutas de entrada del script son absolutas (`data/inputs/...`); ajustar la variable `R`. Requiere `numpy`, `pandas` y `scipy`; ejecutar con `PYTHONIOENCODING=utf-8`.
