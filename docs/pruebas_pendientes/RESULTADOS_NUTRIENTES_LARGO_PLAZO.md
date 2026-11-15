# Resultados: nutrientes y masas de agua, largo plazo

Preregistro confirmado en commit 7a64339, con enmienda de selftest db6c14f antes de ejecutar datos reales. Conclusión: **no se detecta vínculo con estos datos**.

## Método confirmatorio

Reanálisis, no observaciones directas. Veinte predictores en 200–500 m, diez objetivos y seis retrasos; 1998–2025. Se reutilizan cargar/pn de bloque 1 y parcial_multi/corr_neff/fdr de utils, sin modificarlos. Anomalías recentradas por mes; Niño 1+2 en t y t-k; r cruda y parcial sobre los mismos pares completos. FDR sobre las 1200 filas, p=1 para filas no calculables. No se rellenan huecos. Mitades y exclusiones afectan ambos instantes; se exige el signo completo en ambas mitades. ONI se aplica a los que pasan antes del filtro positivo, sin añadir un criterio nuevo.

Sustitutos: 2000 desplazamientos por fila, offsets en [24,312], con reemplazo (289 offsets posibles). Se rota X antes del lag, no Y ni los controles. Estadístico bilateral |r parcial|; p=(1+excedencias)/(2001). Un sustituto inválido cuenta conservadoramente como excedencia. Selección: top 20 p parciales y todos con q<.05. No es un test máximo sobre retrasos. Tamaño efectivo AC1 de residuos y p con neff-2, exactamente como utils, sin descuento explícito de controles.

## Conteos desde las tablas

| Filtro | Número |
| --- | --- |
| Familia primaria | 1200 |
| Calculables | 1200 |
| p cruda < .05 | 69 |
| q cruda < .05 | 0 |
| p parcial < .05 | 123 |
| q parcial < .05 | 0 |
| Mismo signo en mitades (toda la familia) | 504 |
| p sin extremos < .05 (toda la familia) | 119 |
| Sustitutos evaluados | 20 |
| Sustitutos p < .05 (selección calibrada) | 16 |
| q + sustitutos | 0 |
| + signo consistente en mitades | 0 |
| + p sin extremos < .05 | 0 |
| + signo positivo (hallazgos) | 0 |
| Signo inesperado | 0 |

## Pares más altos, aunque no sean hallazgos

| test_id | predictor | target | lag_months | raw_r | partial_r | partial_neff | partial_p | partial_q | p_empirical | half1_r | half2_r | noext_p |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 145 | bellingshausen\|intermediate_200_500m\|o2 | peru_humboldt\|surface_0_5m\|chl | 12 | 0.4249332 | 0.51890216 | 55.65210757 | 4.428e-05 | 0.0531366 | 0.00049975 | 0.6024322 | 0.00947071 | 0.00019372 |
| 445 | peninsula_antarctica\|intermediate_200_500m\|o2 | peru_humboldt\|surface_0_5m\|chl | 12 | 0.39674583 | 0.49121225 | 55.85369622 | 0.00012362 | 0.05323542 | 0.00049975 | 0.58360329 | -0.11761275 | 0.00106404 |
| 1166 | south_pacific_subtropical\|intermediate_200_500m\|so | peru_humboldt\|surface_0_5m\|chl | 24 | -0.3952699 | -0.47282352 | 60.17626633 | 0.00013309 | 0.05323542 | 0.00649675 | -0.44766001 | -0.36411069 | 0.00190794 |
| 865 | south_pacific_intermediate\|intermediate_200_500m\|so | peru_humboldt\|surface_0_5m\|chl | 12 | -0.37728413 | -0.4611775 | 56.85763949 | 0.00031128 | 0.08979818 | 0.08295852 | -0.49025726 | -0.07746215 | 0.00098646 |
| 1164 | south_pacific_subtropical\|intermediate_200_500m\|so | peru_humboldt\|surface_0_5m\|chl | 0 | -0.38254537 | -0.43587429 | 60.49653662 | 0.00047219 | 0.08979818 | 0.01749125 | -0.34321246 | -0.18861477 | 0.00021798 |
| 1165 | south_pacific_subtropical\|intermediate_200_500m\|so | peru_humboldt\|surface_0_5m\|chl | 12 | -0.32868653 | -0.43322278 | 60.09993955 | 0.00053914 | 0.08979818 | 0.04247876 | -0.35918712 | -0.11342894 | 0.00894795 |
| 446 | peninsula_antarctica\|intermediate_200_500m\|o2 | peru_humboldt\|surface_0_5m\|chl | 24 | 0.33970193 | 0.43708686 | 56.95828905 | 0.00067816 | 0.08979818 | 0.00349825 | 0.50070504 | -0.22126954 | 0.00284391 |
| 866 | south_pacific_intermediate\|intermediate_200_500m\|so | peru_humboldt\|surface_0_5m\|chl | 24 | -0.32761511 | -0.42767739 | 58.12664969 | 0.00080099 | 0.08979818 | 0.08995502 | -0.43520194 | -0.22059211 | 0.00353202 |
| 868 | south_pacific_intermediate\|intermediate_200_500m\|so | peru_humboldt\|surface_0_5m\|chl | 48 | -0.28961884 | -0.41700363 | 60.59893438 | 0.00086302 | 0.08979818 | 0.01949025 | -0.32542983 | -0.49337143 | 0.00322661 |
| 85 | bellingshausen\|intermediate_200_500m\|po4 | peru_humboldt\|surface_0_5m\|chl | 12 | -0.35144278 | -0.43221815 | 55.22925065 | 0.00095836 | 0.08979818 | 0.00049975 | -0.59191601 | 0.34667867 | 0.00237455 |

Mediana |r| cruda 0.239661; parcial 0.249668. De 0 filas con q cruda <.05, 0 dejan de pasar tras el control Niño 1+2.

Hallazgos a lag 0: 0; a 12–60 meses: 0. Un vínculo contemporáneo no demuestra transporte lento. Negativos que pasan los otros filtros: 0; "signo inesperado, no respalda la hipótesis". CSV supervivientes/oni sin filas significa cero casos elegibles.

## Potencia estimada (exploratoria)

| true_r | lag_months | median_neff | median_power | min_power | max_power |
| --- | --- | --- | --- | --- | --- |
| 0.2 | 0 | 12.27073 | 0.000193 | 4.2e-05 | 0.006608 |
| 0.2 | 12 | 13.55867 | 0.00023 | 4.2e-05 | 0.006151 |
| 0.2 | 24 | 13.567349 | 0.00023 | 4.2e-05 | 0.006613 |
| 0.2 | 36 | 16.173962 | 0.000314 | 4.2e-05 | 0.007849 |
| 0.2 | 48 | 15.613555 | 0.000294 | 4.2e-05 | 0.007221 |
| 0.2 | 60 | 15.951236 | 0.000306 | 4.2e-05 | 0.006832 |
| 0.3 | 0 | 12.27073 | 0.000551 | 4.2e-05 | 0.052137 |
| 0.3 | 12 | 13.55867 | 0.000705 | 4.2e-05 | 0.048117 |
| 0.3 | 24 | 13.567349 | 0.000707 | 4.2e-05 | 0.052176 |
| 0.3 | 36 | 16.173962 | 0.001094 | 4.2e-05 | 0.06303 |
| 0.3 | 48 | 15.613555 | 0.001002 | 4.2e-05 | 0.057525 |
| 0.3 | 60 | 15.951236 | 0.001058 | 4.2e-05 | 0.054101 |
| 0.5 | 0 | 12.27073 | 0.004437 | 4.2e-05 | 0.614784 |
| 0.5 | 12 | 13.55867 | 0.006369 | 4.2e-05 | 0.588131 |
| 0.5 | 24 | 13.567349 | 0.006384 | 4.2e-05 | 0.615032 |
| 0.5 | 36 | 16.173962 | 0.011853 | 4.2e-05 | 0.677167 |
| 0.5 | 48 | 15.613555 | 0.010486 | 4.2e-05 | 0.647293 |
| 0.5 | 60 | 15.951236 | 0.011308 | 4.2e-05 | 0.627038 |

Aproximación Fisher-z con neff, dos controles y Bonferroni .05/1200. No es potencia exacta del criterio compuesto; la potencia conjunta puede ser menor. No estima la probabilidad de que la hipótesis sea verdadera. neff mediano 14.265, mínimo 3.000. Con 28 años y lags de años quedan pocos grados de libertad efectivos. Un nulo no prueba que no exista vínculo lento; el registro no lo detecta con este diseño.

## Datos faltantes y limitaciones

- Ninguna combinación solicitada falta por completo; complete_pairs de cada fila registra la disponibilidad real.

Niño 1+2 disponible 336 meses; ONI 336. Los lags recortan la muestra y se excluyen cruces entre mitades. No se incluyeron afloramiento calculado, trazadores, perfiles Argo/BGC-Argo ni biomasa acústica; se necesitan esas mediciones y registros más largos e independientes para probar rutas y efectos biológicos. thetao/so no identifican por sí solos masas ni trayectorias.

AC1 no representa toda la memoria de baja frecuencia. Hay dependencia entre regiones/productos del mismo modelo. Los desplazamientos circulares introducen una unión artificial del registro y no representan 2000 historias independientes. Pocos grados efectivos, no estacionariedad y huecos limitan la interpretación. Ni un positivo demostraría transporte o causalidad. No se probaron otros lags/regiones; solo potencia se declara exploratoria.

## Selftest y error observado

El primer selftest pasó la señal sintética a 24 meses (r=0.986749, q=1.02301e-243, p empírico=0.00049975), pero su aserción sobre dos ondas deterministas falló (AssertionError: 0.0004997501249375312). No se ocultó ni se cambió el criterio de sustitutos. Se registró la enmienda db6c14f antes de datos reales para usar el nulo pedido de ruido autocorrelacionado: dos AR(1) independientes, coeficiente .98, semilla 20261117 y 1000 pasos de calentamiento. Ese selftest pasó (r=-0.091326, p empírico=0.548226). La señal y el ruido se verificaron con 2000 sustitutos cada uno. Para la señal, la corrección q usa una familia sintética de 1200 con las restantes p=1; no es una simulación de potencia de toda la búsqueda.

El falso positivo de las ondas se conserva como diagnóstico exploratorio: la restricción de offsets puede dar una calibración inadecuada con formas no estacionarias. Un único ejemplo de ruido que pasa no valida en general el nivel de falsos positivos. Esto refuerza la cautela, incluso para los pares reales con p empírico pequeño.

## Verificación

Se ejecutó dos veces con la misma semilla: los siete CSV y metadatos JSON resultaron idénticos byte por byte (SHA256). Los hashes de entradas se registraron sin modificar originales. Una comprobación inicial del script verificador emitió Pandas4Warning por float_precision; se sustituyó ese argumento por conversores float explícitos y se repitió la verificación.

Una fila calculable al azar, semilla 20261116, se verifica con scipy.linalg.lstsq y scipy.stats.pearsonr; p efectivo con t de SciPy. Coincide a tolerancia 1e-10 (ver verificacion.csv). No se confunde el p de Pearson independiente con el p efectivo. El informe se genera desde CSV y --verify-report revisa conteos y criterios.

Ejecutar con PYTHONIOENCODING=utf-8 y sin -I: python docs/pruebas_pendientes/bloque5_nutrientes_largo_plazo.py --selftest; luego sin opciones. --report-only regenera el informe, --verify-report comprueba las cifras. Semilla 20261115. Versiones: {'python': '3.12.10', 'numpy': '2.5.2', 'pandas': '3.1.0', 'scipy': '1.18.1'}. Hashes SHA256 de entradas en metadatos.json.
