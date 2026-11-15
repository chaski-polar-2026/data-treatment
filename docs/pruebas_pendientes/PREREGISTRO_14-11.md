# Preregistro de pruebas (14/11/2026): teleconexión, perspectiva y desembarques

Se escribe antes de correr las pruebas. Toda prueba posterior no listada aquí se informará como **exploratoria**. Datos locales únicamente (sin descargas).

## Reglas comunes
- Anomalías mensuales (se quita la media de cada mes del calendario) sobre 1998-01 a 2025-12.
- Correlación de Pearson con p calculado con tamaño efectivo de muestra por autocorrelación de orden 1; FDR de Benjamini-Hochberg sobre toda la familia de cada bloque.
- Versiones de comprobación: sin 1998, 2016 y 2023; dos mitades (1998-2011 y 2012-2025: se exige el mismo signo en ambas); primeras diferencias.
- Se reportan todas las pruebas y el tamaño de cada familia.
- Criterio para llamar "hallazgo": q < 0,05 dentro de la familia, mismo signo en las dos mitades y p < 0,05 sin los años extremos.

## Bloque 1. Teleconexión Antártida → costa peruana
- Familia: 8 predictores × 16 objetivos × 7 retrasos (0, 1, 2, 3, 6, 9 y 12 meses; el predictor precede al objetivo) = 896 pruebas.
- Predictores (8): índice SAM; anomalía de la extensión del hielo marino antártico; TSM anómala de Rey Jorge y de la Península Antártica (monitor); temperatura anómala 0-5 m de bellingshausen, peninsula_antarctica, south_pacific_intermediate y south_pacific_subtropical (panel de conectividad).
- Objetivos (16): TSM anómala de las 5 zonas peruanas; clorofila (anomalía en %) de las 5 zonas; panel peru_humboldt: temperatura anómala a 100-200 m, oxígeno anómalo a 100-200 m, nitrato anómalo 0-5 m y clorofila anómala 0-5 m; panel transition_humboldt: temperatura anómala 0-5 m y clorofila anómala 0-5 m.
- Control: correlación parcial controlando el Niño 1+2 (nino12_psl_c); repetición controlando el ONI (oni_c) para los pares que pasen el criterio.
- Medida de causa común: por prueba, r cruda frente a r parcial; número de pruebas con q < 0,05 en la cruda que dejan de serlo al controlar El Niño.

## Bloque 2. Índices PSA y Mar de Amundsen
No existen en disco. Se deja `prueba_indices_externos.py` listo para un CSV (fecha, indice, valor) y una prueba con datos sintéticos. Sin resultados hasta tener el archivo.

## Bloque 3. Perspectiva de condiciones del mar (retrospectiva mensual)
- Objetivos (10): TSM de las 5 zonas peruanas y log de la clorofila de las 5 zonas. Horizontes: 1, 2 y 3 meses. Orígenes: cada mes de 2010-01 a 2025-12 (para pronosticar el mes t se usan solo datos hasta t menos el horizonte).
- Modelos: climatología (referencia), persistencia, persistencia amortiguada (coeficiente ajustado con datos de entrenamiento) y regresión sobre anomalía actual y Niño 1+2 actual. Variante: sin 1998 en el entrenamiento.
- Métricas: error absoluto medio y raíz del error cuadrático; mejora relativa frente a la climatología con IC 95 % por remuestreo de años; acierto del signo.
- Criterio: mejora clara si el IC excluye 0 y se mantiene sin 1998. Los datos son mensuales: no se habla de semanas.

## Bloque 4. Desembarques de anchoveta (BCRP, 2003-2026)
- Objetivo: log(1 + desembarque total mensual). Orígenes 2010-2025, horizontes 1 y 3 meses. Modelos: climatología mensual frente a climatología más anomalía del Niño 1+2 (rezagos fijos de 1, 2 y 3 meses, los tres reportados). Métricas como en el bloque 3, en todos los meses y en los meses con desembarque.
- Limitación declarada: el registro empieza en 2003, así que el evento 1997-98 no está en el entrenamiento; las vedas generan ceros.
