# Entradas reproducibles

La única variable de configuración de entradas es `CHASKI_DATA`; por defecto apunta a esta carpeta, independientemente de la carpeta actual. Se conserva la jerarquía relativa de los insumos originales. Copia local incorporada el 2026-11-15. La fecha de copia no es la fecha de descarga: donde no consta esta última, queda **por verificar**. No se incluyen credenciales ni archivos de entorno.

Los dos monitores comparados tienen los mismos campos y valores, y son idénticos byte a byte. Se usa una copia de `src/nasahackaton/monitor_data.json` del repositorio, no una versión distinta. Resultado estructural en `monitor_comparison.json`.

`manifest.json` es el inventario auditable. El panel es una salida ya procesada de `scripts/11_build_connectivity_panel.py` sobre los productos Copernicus Marine; regenerarlo desde productos crudos requiere esos productos y no forma parte de la reproducción sin red. FAO y NSIDC se conservan como archivos locales existentes; si no consta el script de su obtención, no se infiere. Las tablas auxiliares de monitor se conservan como entradas históricas; su productor exacto está por verificar.

## Inventario

| Entrada relativa a CHASKI_DATA | Bytes | SHA-256 | Procedencia / generador |
|---|---:|---|---|
| `drive_aaron/connectivity_panel_monthly.csv` | 3066314 | `ad7ac9119d2cd326595fa32758a3e5a88044c9c600bc476b2920221cd4b705a9` | Local connectivity panel from Copernicus Marine products; scripts/11_build_connectivity_panel.py |
| `pruebas/json_pagina/monitor_data.json` | 773213 | `ca2a888e326a0f87cae10c94ae37f0fd75835d4a43aed95f3712efc102d248c5` | Committed src/nasahackaton/monitor_data.json; byte-identical to the external analysis copy; scripts/web_export/construir_monitor_json.py |
| `datos/pesquerias/fao_series.csv` | 86347 | `740c88938fca9f9df644cdb802f2da30bc8a9effa0a8464063530a0bd43181f2` | Local processed data; upstream provenance see source catalogue; por verificar |
| `datos/pesquerias/hielo_antartico_nsidc/S_01.csv` | 2352 | `ab782f15f3fb878f5c668e29095f200790ca5fa73805508b4ee78a273e3a0a86` | Local processed data; upstream provenance see source catalogue; por verificar |
| `datos/pesquerias/hielo_antartico_nsidc/S_02.csv` | 2352 | `ee9717d02fbc7f5ad66fb6982d3a5cb746c02a011311f2419f1483384ce9f8b3` | Local processed data; upstream provenance see source catalogue; por verificar |
| `datos/pesquerias/hielo_antartico_nsidc/S_03.csv` | 2352 | `569eb0d2eeb49ffb195d623476998aab9d5b0d3f4b9657a34bef7a818556c92f` | Local processed data; upstream provenance see source catalogue; por verificar |
| `datos/pesquerias/hielo_antartico_nsidc/S_04.csv` | 2352 | `0970d41942ff99a4bc15cfba95d7e4ed944db774e9fd79ecbc0af4e7a98d2139` | Local processed data; upstream provenance see source catalogue; por verificar |
| `datos/pesquerias/hielo_antartico_nsidc/S_05.csv` | 2361 | `65bee706e7aabae72e1fc9c8bc37ad21009d1415ff7a49002dab469e2c9b3555` | Local processed data; upstream provenance see source catalogue; por verificar |
| `datos/pesquerias/hielo_antartico_nsidc/S_06.csv` | 2352 | `ccbe22a3b01f37d48405a6f7898fc63fde30e740f45d29d775f526b5ce875b1e` | Local processed data; upstream provenance see source catalogue; por verificar |
| `datos/pesquerias/hielo_antartico_nsidc/S_07.csv` | 2352 | `eabbacf263faf23a01b8db13252a798485a8a5ef4294a6fbdae5aa0c9af9b527` | Local processed data; upstream provenance see source catalogue; por verificar |
| `datos/pesquerias/hielo_antartico_nsidc/S_08.csv` | 2352 | `64c76142efc35e76f8e593d90e958621cee9ca0a104d3b337494deb3dbcdc2e8` | Local processed data; upstream provenance see source catalogue; por verificar |
| `datos/pesquerias/hielo_antartico_nsidc/S_09.csv` | 2352 | `32e94df4721daf475d675490ce81d49d5e99f47e43cad2660c064ab56ba4f01a` | Local processed data; upstream provenance see source catalogue; por verificar |
| `datos/pesquerias/hielo_antartico_nsidc/S_10.csv` | 2304 | `c2c343b117cb1e04c8f08821ee9982c124312d3cce59c86e90f0a75b6ee8af4e` | Local processed data; upstream provenance see source catalogue; por verificar |
| `datos/pesquerias/hielo_antartico_nsidc/S_11.csv` | 2352 | `1ad02149c0e754021fb136324550bcb171390805e34ea0501b8136874f1f4e5a` | Local processed data; upstream provenance see source catalogue; por verificar |
| `datos/pesquerias/hielo_antartico_nsidc/S_12.csv` | 2352 | `dafcb0df80ac1fb828ae66bb40f28b10539ace084b0a9fb2e19cef145abe1dc2` | Local processed data; upstream provenance see source catalogue; por verificar |
| `datos/peru/variables_mensuales.csv` | 964759 | `81057fe62437168452f88f59f6f9284e16e28dab391f1e8232c5bc09b9808860` | Local processed data; upstream provenance see source catalogue; por verificar |
| `datos/oni.txt` | 23025 | `5d6fa3a2f857d916550d39c2c686e94cb942430195c82518e6a5d0f5ffbd0665` | Local processed data; upstream provenance see source catalogue; por verificar |
| `datos/aao.data` | 3990 | `4b2b62b0b8460f693d1960b237622f3e4100aa476f141f857272dee315cf78a4` | Local processed data; upstream provenance see source catalogue; por verificar |
| `repo/data/nino12.long.anom.csv` | 41530 | `98f68edaa8bcea8560823c6fe491c8abcdbc83c5d5f1eaeda453aff2bb12b8b0` | Repository committed input; por verificar |
| `repo/data/raw/nsidc/S_seaice_extent_daily_v4.0.csv` | 1852523 | `d0b5148e45a83698ba3223574f4f1d20304ee5896a3e7f7d66b96ecc534dc2a2` | Repository committed input; scripts/01_download_data.py |
| `repo/data/punto1_anchoveta/1a_desembarques_mensuales_bcrp/desembarques_anchoveta_mensual_2003_2026.csv` | 19095 | `0af0020951051068ff139177fd4879ea7204f5d9deb27c59c02a8fbdb8075191` | Repository committed input; por verificar |
| `pruebas/fitoplancton/tablas/h1d_eventos_pct.csv` | 479 | `c9ce303a8a6c91b259cb33e671b16b6ae59f7fb8c7f557440aa26a788ae2bba4` | Existing local analysis table; por verificar; historical analysis scripts |
| `pruebas/fitoplancton/tablas/dif_asimetria_temperatura_local.csv` | 501 | `919b9fea7321880be9bf40139289ddd246760b4605698bbb7906545ce5705838` | Existing local analysis table; por verificar; historical analysis scripts |
| `web/el-nino-chain.json` | 61115 | `38a242506e338d130e68a182a5cd2cf84ed984a9a775a5dbc1f47a3ffbe25f36` | Web physical-chain data; por verificar |
| `web/monitor-data-base.js` | 680297 | `1901b6505a4672fdd870a829d54c0fce55e032ff874437b870298a4cacc3620b` | Previous monitor read by original constructor; por verificar |
| `datos/tendencias_largas/ersstv5_sst_mnmean.nc` | 162376295 | `952fad739abab3e3c33c955b168f298b9884d2fe48ab259ebf19ac531d8d8386` | NOAA PSL ERSST v5; https://downloads.psl.noaa.gov/Datasets/noaa.ersst.v5/sst.mnmean.nc; external download; exact retrieval script/date por verificar |

## ERSST: descarga separada, nunca en Git

El archivo usado localmente se llama `ersstv5_sst_mnmean.nc`. Proveedor: NOAA PSL; ERSST v5, media mensual SST global de 2 grados. Enlace oficial del archivo: https://downloads.psl.noaa.gov/Datasets/noaa.ersst.v5/sst.mnmean.nc . Guardarlo con el nombre local indicado bajo `datos/tendencias_largas/` dentro de CHASKI_DATA. El archivo remoto puede actualizarse: comparar SHA-256 con el inventario antes de afirmar identidad. El snapshot exacto histórico, su fecha de descarga y su disponibilidad remota están por verificar; un hash distinto no se debe sustituir silenciosamente.

No se incorpora el NetCDF grande al repositorio. El exportador falla con `Missing input: datos/tendencias_largas/ersstv5_sst_mnmean.nc` si falta. La prueba local usó el archivo histórico en una carpeta temporal externa. Los bloques 1, 3, 4, 5 y vecinos no necesitan ERSST.

## Entradas del constructor web

`web/monitor-data-base.js` es la copia previa que leía el constructor original; es una entrada, no el monitor publicado actual. `web/el-nino-chain.json` alimenta las relaciones con Niño. `datos/peru/variables_mensuales.csv`, `repo/data/nino12.long.anom.csv`, `datos/oni.txt`, `datos/aao.data`, el hielo diario y las dos tablas históricas del inventario son dependencias directas de construcción; no se recalculan análisis nuevos. El constructor solo importa bibliotecas estándar, numpy y pandas; no tiene módulos locales adicionales.

Los scripts históricos fuera de la ejecución conjunta pueden pedir otros insumos no incluidos (Giovanni, mareógrafos, mapas o `datos.js`). Sus rutas ya son configurables; no se inventan ni descargan esos archivos. Si se necesita reproducirlos, completar el inventario primero. La reproducción solicitada y los tres exportadores usan únicamente los insumos enumerados aquí.
