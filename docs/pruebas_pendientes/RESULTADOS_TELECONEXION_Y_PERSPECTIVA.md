# Resultados: teleconexión Antártida → Perú, perspectiva de condiciones del mar y desembarques

Fecha: 14/11/2026. Preregistro: `PREREGISTRO_14-11.md` (commit anterior a los resultados). Scripts: `bloque1_teleconexion.py`, `prueba_indices_externos.py`, `bloque3_perspectiva.py`, `bloque4_desembarques.py` (más `utils_pruebas.py`). Tablas en `data/tablas_pruebas_pendientes/`; JSON de acierto en `data/perspectiva_acierto.json`. Solo datos locales, sin descargas.

## Resumen
1. **Teleconexión (bloque 1): no hay vínculo.** De 896 pruebas, ninguna supera el FDR, ni en correlación cruda ni controlando El Niño.
2. **Índices PSA y Mar de Amundsen (bloque 2): no hay datos en disco.** El script queda listo y probado con datos sintéticos.
3. **Perspectiva (bloque 3): la temperatura del mar se anticipa bien a 1 a 3 meses; la clorofila, poco.** Mejora clara a 1 mes en la temperatura de las 5 zonas; en clorofila, solo a 1 mes y en 3 o 4 zonas.
4. **Desembarques de anchoveta (bloque 4): El Niño no mejora la predicción de los desembarques mensuales** frente a la climatología mensual. Se mantiene la alerta con antecedentes históricos, sin "tendencia esperada de desembarques".

## Bloque 1. Señales antárticas frente a la costa peruana
- Familia: 8 predictores × 16 objetivos × 7 retrasos = 896 pruebas (preregistro). Control: correlación parcial controlando el Niño 1+2 **en el instante del objetivo y en el del predictor** (así se implementó "controlar El Niño", un control más estricto que usar solo uno).
- Con p < 0,05 en la correlación cruda hay 82 pruebas (por azar se esperarían unas 45; las pruebas no son independientes). Con q (FDR) < 0,05: **0 en la cruda y 0 en la parcial**.
- Mediana de |r|: 0,068 (cruda) y 0,064 (parcial). Como ninguna correlación cruda supera el FDR, la medida de "causa común" (cuántas relaciones desaparecen al controlar El Niño) no se puede evaluar: 0 de 0.
- Los valores más altos tras controlar El Niño son r ≈ 0,3 entre la temperatura del Pacífico sur subtropical e intermedio y la clorofila de 0-5 m de Humboldt (reanálisis), y entre la temperatura de la Península Antártica con 12 meses de adelanto y la clorofila de transición; todos con q = 0,27. No son hallazgos.
- Verificación independiente: SAM → clorofila de Chimbote a 6 meses, r = −0,2071 con SciPy y con el cálculo propio, y coincide con la tabla.

## Bloque 2. Índices PSA, Mar de Amundsen y altura geopotencial
No existen en disco (revisado). Para ejecutar el bloque falta: índices PSA1 y PSA2 mensuales, índice del Mar de Amundsen y altura geopotencial a 500 hPa, 1998-2025 (**por verificar** proveedor y archivo exacto). El script `prueba_indices_externos.py ruta.csv` (columnas fecha, indice, valor) aplica la misma familia y el mismo control; `--selftest` pasa (recupera una relación sintética a 2 meses de retraso).

## Bloque 3. Perspectiva retrospectiva (mensual, 2010-2025)
Orígenes móviles: para el mes t y el horizonte h solo se usan datos hasta t−h. Mejora relativa del error absoluto medio frente a la climatología (mediana de las 5 zonas); "claras" = zonas donde el IC 95 % excluye 0 con y sin 1998 en el entrenamiento.

| Variable | Horizonte | Mejora (modelo con Niño) | Zonas con mejora clara | Acierto del signo (base 50 %) |
|---|---|---|---|---|
| TSM | 1 mes | 44 % | 5 de 5 | 82 % |
| TSM | 2 meses | 28 % | 5 de 5 | 74 % |
| TSM | 3 meses | 18 % | 5 de 5 | 66 % |
| Clorofila (log) | 1 mes | 15 % | 4 de 5 | 70 % |
| Clorofila (log) | 2 meses | 7 % | 1 de 5 | 64 % |
| Clorofila (log) | 3 meses | 4 % | 2 de 5 | 63 % |

- La persistencia sola es peor que la climatología para la clorofila a 2 y 3 meses (−20 % y −35 %); el modelo amortiguado o con El Niño corrige eso.
- 45 de las 90 combinaciones (zona × horizonte × modelo) tienen mejora clara con y sin 1998.
- Verificación independiente: la mejora de la TSM de Callao a 1 mes con persistencia (0,4546) coincide con 1 − MAE modelo / MAE climatología recalculado desde la tabla.
- **Límite:** datos mensuales; no se pueden hacer afirmaciones sobre semanas. El acierto se midió en meses pasados y no garantiza el futuro. El archivo `data/perspectiva_acierto.json` trae el acierto por zona, variable y horizonte con el estado "clear improvement" o "no clear improvement".

## Bloque 4. Desembarques mensuales de anchoveta (BCRP, 2003-2026)
- 14 de 276 meses tienen desembarque cero (vedas). Orígenes 2010-2025; horizontes 1 y 3 meses; Niño 1+2 con rezago fijo de 1, 2 o 3 meses (solo es utilizable si el rezago es mayor o igual al horizonte).
- Mejora frente a la climatología mensual: entre −0,0 % y +1,2 % en todos los meses, con IC 95 % que incluye cero. En los meses con desembarque y sin 2016, 2017 y 2023 en el entrenamiento aparecen dos casos con +1,7 % y límite inferior apenas sobre cero (0,001), en una prueba no central: una mejora despreciable.
- **Conclusión:** El Niño no mejora la predicción mensual de los desembarques de anchoveta en 2010-2025. Los desembarques dependen sobre todo de la estacionalidad, las cuotas y las vedas. La alerta pesquera debe presentarse con antecedentes históricos, no como "tendencia esperada de desembarques".
- Desviación del preregistro: el registro empieza en 2003, así que el evento 1997-98 no está en el entrenamiento. La variante usada fue quitar 2016, 2017 y 2023 del entrenamiento.

## Advertencias
- Todas las pruebas de cada bloque están en las tablas CSV. Nada se presentó como hallazgo sin superar el FDR, mantener el signo en las dos mitades y sobrevivir sin los años extremos.
- Los desembarques no miden la abundancia. La perspectiva describe condiciones del mar, no presencia de peces.
- No se incluyeron pruebas exploratorias fuera del preregistro.
