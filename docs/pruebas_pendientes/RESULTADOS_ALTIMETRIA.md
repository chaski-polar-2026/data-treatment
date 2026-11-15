# Altimetría frente al Perú y GLORYS

## Conclusión
**Coinciden parcialmente**, según la regla descriptiva de signo y solapamiento de intervalos individuales. No es una prueba formal de igualdad; no se define una conclusión fuerte de coincidencia sin evaluar incertidumbre conjunta y dependencia.

Correlación mensual (1998–2025): r = 0.977; meses comunes: 336.
Diferencia de pendientes (altimetría − GLORYS): +0.409 cm/década.

## Tendencias

| Serie | Inicio | Sin 1998, 2016, 2023 | n | Sen cm/década | IC 95 % | p | q FDR (12) |
|---|---:|---|---:|---:|---|---:|---:|
| Altimetría SLA | 1998 | no | 28 | 2.995 | [2.242, 3.745] | 1.2435e-06 | 4.9741e-06 |
| Altimetría SLA | 1998 | sí | 25 | 2.985 | [2.410, 3.688] | 3.2207e-08 | 3.8648e-07 |
| Altimetría SLA | 2003 | no | 23 | 3.138 | [2.377, 4.200] | 1.031e-05 | 1.6909e-05 |
| Altimetría SLA | 2003 | sí | 21 | 2.868 | [2.083, 3.742] | 1.1272e-05 | 1.6909e-05 |
| Altimetría SLA | 2010 | no | 16 | 3.481 | [1.151, 5.561] | 0.015155 | 0.015155 |
| Altimetría SLA | 2010 | sí | 14 | 2.808 | [1.151, 4.346] | 0.009753 | 0.013004 |
| GLORYS zos | 1998 | no | 28 | 2.586 | [1.962, 3.288] | 2.6237e-06 | 7.8711e-06 |
| GLORYS zos | 1998 | sí | 25 | 2.566 | [1.984, 3.087] | 9.9636e-08 | 5.9782e-07 |
| GLORYS zos | 2003 | no | 23 | 2.865 | [2.111, 3.948] | 3.9052e-06 | 9.3724e-06 |
| GLORYS zos | 2003 | sí | 21 | 2.647 | [1.976, 3.443] | 7.786e-06 | 1.5572e-05 |
| GLORYS zos | 2010 | no | 16 | 2.658 | [0.763, 4.866] | 0.011481 | 0.013777 |
| GLORYS zos | 2010 | sí | 14 | 2.276 | [0.763, 3.859] | 0.013838 | 0.015096 |

## Método y límites

Caja −85 a −70° longitud y −18,35 a −3,38° latitud. Mediana espacial mensual en ambas fuentes; el CSV incluye además media altimétrica ponderada por área y cobertura. Solo meses comunes en 1998–2025. Se resta climatología mensual, se exige 9 meses por año, se aplica Kendall, Sen e intervalo por rangos de Gilbert como en la ronda original. FDR BH sobre las 12 pruebas de esta comparación; no es la familia histórica de 162 y sus q no son comparables directamente.
Las pruebas anuales no corrigen autocorrelación; los intervalos son individuales. Las series interpoladas L4 no son mediciones puntuales. GLORYS asimila datos altimétricos, por lo que la comparación no constituye validación plenamente independiente. SLA y zos tienen referencias diferentes; se centran para la correlación y figura.
Las correcciones de marea y ajuste isostático deben verificarse en los metadatos del archivo y el manual. El manual describe tpa_correction, una corrección posterior de deriva instrumental TOPEX-A, y señala que puede aplicarse regionalmente como aproximación; aquí no se ha aplicado. No se ha confirmado el tratamiento de GIA ni de las mareas para esta versión. Los atributos time_coverage originales pueden corresponder a un archivo fuente; la cobertura efectiva debe verificarse en las coordenadas temporales.

Dataset: c3s_obs-sl_glo_phy-ssh_my_twosat-l4-duacs-0.25deg_P1M-m; versión: vNov2024; descarga UTC: 2026-11-14T18:32:57.112496+00:00.
Metadatos globales: `{"Conventions": "CF-1.6", "Metadata_Conventions": "Unidata Dataset Discovery v1.0", "cdm_data_type": "Grid", "comment": "Monthly Mean of Sea Level Anomalies referenced to the [1993, 2012] period", "contact": "http://climate.copernicus.eu/c3s-user-service-desk", "creator_email": "http://climate.copernicus.eu/c3s-user-service-desk", "creator_name": "Copernicus Climate Change Service (C3S)", "creator_url": "http://climate.copernicus.eu", "date_created": "2024-11-05T23:40:10Z", "geospatial_lat_max": "89.875", "geospatial_lat_min": "-89.875", "geospatial_lat_resolution": "0.25", "geospatial_lat_units": "degrees_north", "geospatial_lon_max": "179.875", "geospatial_lon_min": "-179.875", "geospatial_lon_resolution": "0.25", "geospatial_lon_units": "degrees_east", "geospatial_vertical_max": "0.0", "geospatial_vertical_min": "0.0", "geospatial_vertical_positive": "down", "geospatial_vertical_resolution": "point", "geospatial_vertical_units": "m", "history": "2024-11-05T23:40:10Z: Creation", "institution": "CLS, CNES", "keywords": "Oceans > Ocean Topography > Sea Surface Height", "keywords_vocabulary": "NetCDF COARDS Climate and Forecast Standard Names", "license": "http://climate.copernicus.eu/c3s-user-service-desk", "processing_level": "L4", "product_version": "vNov2024", "project": "Copernicus Climate Change Service (C3S)", "references": "http://climate.copernicus.eu", "software_version": "8.0_DUACS_DT2024_baseline", "source": "Altimetry measurements", "ssalto_duacs_comment": "The reference mission used for the altimeter inter-calibration processing is Topex/Poseidon between 1993-01-01 and 2002-04-23, Jason-1 between 2002-04-24 and 2008-10-18, OSTM/Jason-2 between 2008-10-19 and 2016-06-25, Jason-3 since 2016-06-25.", "standard_name_vocabulary": "NetCDF Climate and Forecast (CF) Metadata Convention Standard Name Table v37", "summary": "Delayed Time Level-4 monthly means of Sea Level Anomalies and derived Eddy Kinetic Energy from two-satellite altimetry observations over the Global Ocean.", "time_coverage_duration": "P1M", "time_coverage_end": "2023-12-31T00:00:00Z", "time_coverage_resolution": "P1M", "time_coverage_start": "2023-12-01T00:00:00Z", "title": "DT merged two-satellite Global Ocean L4 Monthly Means of Sea Level Anomalies and Derived Eddy Kinetic Energy", "copernicusmarine_version": "2.5.0"}`

Fuentes: https://data.marine.copernicus.eu/product/SEALEVEL_GLO_PHY_CLIMATE_L4_MY_008_057/description ; https://documentation.marine.copernicus.eu/PUM/CMEMS-SL-PUM-008-057.pdf ; https://documentation.marine.copernicus.eu/QUID/CMEMS-GLO-QUID-001-030.pdf

Salidas: `./data/tablas_pruebas_pendientes/altimetria`.


## Nota de comparabilidad (documentación de reproducción)

Sin sustituir la conclusión del autor: altimetría +3,0 cm/década (IC 95 %: 2,2 a 3,7), GLORYS +2,6 (2,0 a 3,3). Los intervalos individuales se solapan; esto no es una prueba formal de igualdad. GLORYS asimila altimetría, por lo que las fuentes no son plenamente independientes. No está confirmado el tratamiento de mareas, ajuste isostático ni corrección de deriva TOPEX-A del producto usado. Estos puntos quedan como límites de la comparación, sin añadir correcciones ni recalcular resultados.
