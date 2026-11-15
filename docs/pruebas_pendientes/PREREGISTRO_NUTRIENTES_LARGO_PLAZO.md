# Preregistro: nutrientes y masas de agua, largo plazo

Fecha: 2026-11-15. Rama: analisis/nutrientes-largo-plazo. Base: main 48d75b8. Solo archivos locales; no se modifican datos ni resultados anteriores. Este documento se confirma antes de ejecutar pruebas, selftest o inspeccionar correlaciones.

## Diseño preregistrado (texto solicitado)

- Predictores (20): para cada una de las 4 regiones del sur (bellingshausen, peninsula_antarctica, south_pacific_intermediate, south_pacific_subtropical), banda intermediate_200_500m, las anomalías mensuales de no3, po4, o2, thetao y so.
- Objetivos (10): para peru_humboldt y para transition_humboldt: no3 en surface_0_5m, no3 en subsurface_100_200m, po4 en subsurface_100_200m, o2 en subsurface_100_200m y chl en surface_0_5m.
- Retrasos (el predictor precede al objetivo): 0, 12, 24, 36, 48 y 60 meses. Familia primaria: 20 × 10 × 6 = 1200 pruebas.
- Control: correlación parcial (parcial_multi de utils) controlando el Niño 1+2 en el instante del objetivo y en el del predictor. Repite con el ONI para los pares que pasen el criterio.
- Estadística: anomalías mensuales sin ciclo estacional, correlación con tamaño efectivo por autocorrelación, FDR de Benjamini-Hochberg sobre las 1200 pruebas.
- Calibración extra por sustitutos (solo para los 20 pares con menor p y los que pasen FDR): 2000 desplazamientos circulares aleatorios del predictor (desfase mínimo de 24 meses respecto a la serie original) para obtener un p empírico que respete la autocorrelación de baja frecuencia.
- Versiones de comprobación: sin 1998, 2016 y 2023; dos mitades (1998-2011 y 2012-2025) con el mismo signo exigido.
- Dirección esperada: positiva (más nutriente en el sur, más nutriente después en Perú). Si un par pasa el criterio con signo negativo, repórtalo como "signo inesperado, no respalda la hipótesis".
- Criterio de hallazgo: q < 0,05, p empírico por sustitutos < 0,05, mismo signo en las dos mitades, p < 0,05 sin los años extremos y signo positivo.
- Declarado de antemano: con 28 años y retrasos de varios años quedan pocos grados de libertad efectivos, así que la potencia es baja; un resultado nulo no prueba que no exista un vínculo lento, solo que este registro no lo detecta.

## Implementación fijada antes de resultados

- Entradas: D:/hackathon/NASA/drive_aaron/connectivity_panel_monthly.csv y D:/hackathon/NASA/pruebas/json_pagina/monitor_data.json. Se reutilizan cargar y pn de bloque1_teleconexion.py, y anomalia_mensual, parcial_multi, corr_neff, fdr, EXTREMOS de utils_pruebas.py. Se registran hashes SHA256 y versiones.
- Calendario mensual continuo enero 1998–diciembre 2025. Las columnas *_anom se recentran con anomalia_mensual sobre el registro completo, como en bloque 1. No se rellenan huecos. Se exige al menos 36 pares completos (regla existente). Las combinaciones no calculables permanecen entre las 1200 filas y entran al FDR con p=1. Se documentan variables ausentes, duplicados y conteos; un duplicado región/banda/fecha detiene el proceso.
- Semilla primaria 20261115, generador numpy default_rng. Orden: regiones del sur en el orden escrito, variables no3/po4/o2/thetao/so, regiones objetivo peru_humboldt/transition_humboldt, objetivos en el orden escrito, retrasos en el orden escrito. Desempates del top 20 por índice de prueba, estable.
- Para retraso k se correlacionan X[t-k] y Y[t]; controles [Niño(t), Niño(t-k)]. En k=0 las columnas repetidas se resuelven por mínimos cuadrados, como en utils. r cruda se informa en la misma muestra completa que la parcial. El p efectivo usa exactamente utils (AC1 de residuos; fórmula n_eff, t con n_eff-2); no se añade otra corrección de grados de libertad. Esto es una limitación explícita, sobre todo con huecos o pocas observaciones efectivas.
- Mitades: ambos instantes, t y t-k, deben pertenecer a la misma mitad; evita cruzar 2011/2012. Sin extremos: se excluye el par si cualquiera de los dos instantes pertenece a 1998, 2016 o 2023. No se recalcula climatología dentro de subconjuntos. Signo de cada mitad debe coincidir con el del ajuste completo. Se informa también el signo sin extremos.
- Sustitutos: desplazar circularmente la serie completa de 336 meses antes de aplicar el retraso k y antes de eliminar pares incompletos; offsets enteros en [24, N-24], con reemplazo, 2000 por prueba seleccionada. La distancia circular mínima es 24. Se mantienen Y y controles en sus fechas originales; se recalcula la parcial para cada sustituto. Estadístico bilateral |r parcial|; p=(1+conteo de |r_sustituto|>=|r_observado|)/(1+B). Si algún sustituto no es calculable, se cuenta conservadoramente como excedencia y se informa. No se consideran 2000 offsets únicos: el registro solo permite N-47 offsets. Esto calibra cada par; no es un test máximo sobre toda la búsqueda de retrasos. No se exige que el offset sea múltiplo de 12 porque se trabaja con anomalías sin ciclo estacional.
- Se comprueban mitades y extremos en las 1200 filas. Sustitutos solamente unión de top 20 p parciales finitos y q<.05. ONI: repetir parcial y comprobaciones para las filas que cumplan todos los filtros principales antes de exigir signo positivo, sin redefinir hallazgo ni ajustar otra familia. Se declara corroboración ONI si p<.05 y mismo signo; no añade un requisito al criterio original.
- Se informan por separado resultados de retraso 0 y de 12–60 meses; una asociación contemporánea no es evidencia de transporte lento. Tampoco una asociación cruzada entre distintas variables demuestra transporte de nutrientes ni masa de agua. No se prueban trazadores ni afloramiento.
- Selftest: relación sintética a 24 meses dentro de una familia con corrección de 1200, y dos oscilaciones independientes de baja frecuencia, que no deben superar el filtro de sustitutos. No se usan datos reales para elegir esos ejemplos.
- Comprobación independiente: una fila calculable elegida aleatoriamente con semilla 20261116; residuos mediante scipy.linalg.lstsq, r mediante scipy.stats.pearsonr y p efectivo mediante t de SciPy. Se compara con resultados propios con tolerancia 1e-10.
- Reproducibilidad: dos ejecuciones con misma semilla deben generar CSV idénticos; el informe se construye desde los CSV y se verifican sus conteos.

## Exploratorio, no criterio de hallazgo

Potencia aproximada con transformación Fisher-z normal usando n_eff observado, controles de dos columnas y umbral Bonferroni .05/1200 como referencia conservadora, para r verdadero .2/.3/.5. No es potencia exacta del criterio compuesto (FDR, sustitutos y robustez), que será menor y no se identifica con este cálculo. Todo análisis no listado como confirmatorio se etiqueta exploratorio.

## Archivos de salida

bloque5_nutrientes_largo_plazo.py; CSV nuevos con prefijo bloque5_nutrientes_ en data/tablas_pruebas_pendientes/: todas, supervivientes, sustitutos (2000 filas por prueba seleccionada), calibracion, oni, verificacion y potencia_exploratoria. Informe RESULTADOS_NUTRIENTES_LARGO_PLAZO.md y entrada añadida a SEGUIMIENTO_PRUEBAS.md. Los resultados anteriores no se sobrescriben. Se ejecuta sin -I y con PYTHONIOENCODING=utf-8.

## Enmienda de implementación antes de datos reales

El primer selftest pasó la señal de 24 meses (q=1.02301e-243, p empírico=0.00049975), pero falló el supuesto nulo de ondas deterministas: p empírico=0.00049975. Dos senos de períodos 240/260 meses no son ruido de innovaciones independientes, y la restricción de offsets puede producir falsos positivos con esas formas no estacionarias. Se conserva ese ejemplo como diagnóstico y se informa su fallo; no se cambia el test de sustitutos ni el criterio confirmatorio.

Para la prueba nula pedida de ruido autocorrelacionado se fija, sin consultar datos reales, ruido AR(1) de coeficiente .98, dos innovaciones independientes, semilla 20261117, 1000 meses de calentamiento y 336 retenidos. La semilla primaria y los 2000 draws reales no cambian. Esta enmienda se confirma antes de ejecutar el AR(1) y los datos reales. Un solo nulo sintético no demuestra control general de falsos positivos.
