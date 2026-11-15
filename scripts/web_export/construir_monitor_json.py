import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"docs/pruebas_pendientes"))
from config_datos import DATA, ROOT, WEB_EXPORT, require
"""Construye monitor_data.json (y monitor-data.js) para el Monitor de la web y para Google Colab.

- Conserva todos los campos del monitor-data.js actual (mismo formato: records + metadata).
- Agrega por mes: clorofila y temperatura de 7 zonas (valor y anomalía), Niño 1+2, ONI, SAM
  y extensión del hielo antártico.
- metadata: fuentes, diccionario de variables, zonas, eventos El Niño y hallazgos.
No modifica ningún archivo de los repositorios: escribe en pruebas/json_pagina/.
"""
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

BASE = DATA
OUT = WEB_EXPORT
WEB = require("web/monitor-data-base.js")
REPO = DATA / "repo"
TAB = BASE / "pruebas" / "fitoplancton" / "tablas"

ZONAS = {
    "paita": ("peru_norte_paita_sechura", "Paita-Sechura", "peru", (-6.5, -4.5, -82.0, -80.5)),
    "chimbote": ("peru_centro_norte_chimbote", "Chimbote", "peru", (-10.0, -8.0, -80.0, -78.0)),
    "callao": ("peru_centro_callao", "Callao", "peru", (-13.0, -11.0, -78.5, -76.8)),
    "pisco": ("peru_sur_pisco", "Pisco", "peru", (-14.5, -13.0, -77.0, -76.0)),
    "ilo": ("peru_sur_ilo", "Ilo", "peru", (-18.0, -16.5, -72.5, -71.0)),
    "peninsula_antartica": ("antartida_peninsula", "Península Antártica", "oceano_austral", (-68.0, -60.0, -70.0, -55.0)),
    "rey_jorge": ("antartida_rey_jorge", "Rey Jorge", "oceano_austral", (-63.0, -61.5, -60.5, -56.5)),
}

# ---------------------------------------------------------------- monitor actual
texto = WEB.read_text(encoding="utf-8")
actual = json.loads(texto[texto.index("{"): texto.rindex("}") + 1])
idx = pd.to_datetime([r["date"] for r in actual["records"]])

# ---------------------------------------------------------------- series nuevas
v = pd.read_csv(BASE / "datos" / "peru" / "variables_mensuales.csv")
v["f"] = pd.to_datetime(v.mes + "-01")
w = v.pivot_table(index="f", columns=["variable", "zona"], values="valor")
ref = slice("1998-01-01", "2025-12-01")


def clim_anom(s, log=False):
    s = s.reindex(pd.date_range("1985-01-01", "2026-12-01", freq="MS"))
    x = np.log10(s.where(s > 0)) if log else s
    r = x.loc[ref]
    a = x - x.index.month.map(r.groupby(r.index.month).mean()).to_numpy()
    if log:
        a = (10 ** a - 1) * 100  # % respecto de lo normal para ese mes
    return a.reindex(idx)


nuevas = {}
for clave, (zona, _, _, _) in ZONAS.items():
    chl = w.get(("clorofila_mg_m3", zona))
    sst = w.get(("temperatura_superficial_C", zona))
    nuevas[f"chl_{clave}_mg_m3"] = chl.reindex(idx)
    nuevas[f"chl_{clave}_anom_pct"] = clim_anom(chl, log=True)
    nuevas[f"sst_{clave}_c"] = sst.reindex(idx)
    nuevas[f"sst_{clave}_anom_c"] = clim_anom(sst)

n = pd.read_csv(REPO / "data" / "nino12.long.anom.csv", skiprows=1, names=["f", "v"])
n["f"] = pd.to_datetime(n["f"])
nuevas["nino12_psl_c"] = n.set_index("f")["v"].where(lambda s: s > -90).reindex(idx)

centro = {"DJF": 1, "JFM": 2, "FMA": 3, "MAM": 4, "AMJ": 5, "MJJ": 6, "JJA": 7, "JAS": 8, "ASO": 9, "SON": 10, "OND": 11, "NDJ": 12}
oni = {}
for linea in (BASE / "datos" / "oni.txt").read_text().splitlines()[1:]:
    p = linea.split()
    if len(p) == 4 and p[0] in centro:
        oni[pd.Timestamp(int(p[1]), centro[p[0]], 1)] = float(p[3])
nuevas["oni_c"] = pd.Series(oni).reindex(idx)

sam = {}
for linea in (BASE / "datos" / "aao.data").read_text().splitlines()[1:]:
    p = linea.split()
    if len(p) == 13 and p[0].isdigit():
        for m, x in enumerate(p[1:], 1):
            sam[pd.Timestamp(int(p[0]), m, 1)] = float(x)
nuevas["sam_index"] = pd.Series(sam).where(lambda s: s > -90).reindex(idx)

h = pd.read_csv(REPO / "data" / "raw" / "nsidc" / "S_seaice_extent_daily_v4.0.csv", skiprows=[1], skipinitialspace=True)
h["f"] = pd.to_datetime(dict(year=h.Year, month=h.Month, day=1))
hielo = h.groupby("f")["Extent"].mean()
nuevas["sea_ice_antarctic_mkm2"] = hielo.reindex(idx)
nuevas["sea_ice_antarctic_anom_mkm2"] = clim_anom(hielo)


def limpio(x):
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return None
    return round(float(x), 4)


records = []
for i, r in enumerate(actual["records"]):
    fila = dict(r)  # campos actuales intactos
    for clave, serie in nuevas.items():
        fila[clave] = limpio(serie.iloc[i])
    records.append(fila)

# ---------------------------------------------------------------- metadata
variables = {}
for clave, (zona, nombre, escala, _) in ZONAS.items():
    variables[f"chl_{clave}_mg_m3"] = {"nombre": f"Clorofila-a, {nombre}", "unidad": "mg/m³", "fuente": "occci_v6", "zona": clave}
    variables[f"chl_{clave}_anom_pct"] = {"nombre": f"Clorofila-a respecto de lo normal, {nombre}", "unidad": "%", "fuente": "occci_v6", "zona": clave,
                                          "metodo": "Diferencia con el promedio del mismo mes (1998-2025), en escala logarítmica, expresada en %."}
    variables[f"sst_{clave}_c"] = {"nombre": f"Temperatura superficial, {nombre}", "unidad": "°C", "fuente": "crw_sst", "zona": clave}
    variables[f"sst_{clave}_anom_c"] = {"nombre": f"Anomalía de temperatura superficial, {nombre}", "unidad": "°C", "fuente": "crw_sst", "zona": clave,
                                        "metodo": "Diferencia con el promedio del mismo mes (1998-2025)."}
variables.update({
    "nino12_psl_c": {"nombre": "Índice Niño 1+2 (actualizado)", "unidad": "°C", "fuente": "nino12_psl"},
    "oni_c": {"nombre": "Índice ONI (El Niño en el Pacífico central, trimestre centrado)", "unidad": "°C", "fuente": "oni"},
    "sam_index": {"nombre": "Modo Anular del Sur (vientos antárticos)", "unidad": "adimensional", "fuente": "sam_psl"},
    "sea_ice_antarctic_mkm2": {"nombre": "Extensión del hielo marino antártico", "unidad": "millones de km²", "fuente": "nsidc"},
    "sea_ice_antarctic_anom_mkm2": {"nombre": "Anomalía de extensión del hielo marino antártico", "unidad": "millones de km²", "fuente": "nsidc"},
})

fuentes = dict(actual.get("sources", {}))
fuentes.update({
    "occci_v6": {"nombre": "ESA Ocean Colour CCI v6, clorofila-a mensual 4 km", "tipo": "satelital", "url": "https://comet.nefsc.noaa.gov/erddap/griddap/occci_V6_monthly_4km.html",
                 "procesamiento": "Mediana mensual de los píxeles de cada zona."},
    "crw_sst": {"nombre": "NOAA Coral Reef Watch v3.1, temperatura superficial mensual", "tipo": "satelital", "url": "https://oceanwatch.pifsc.noaa.gov/erddap/griddap/CRW_sst_v3_1_monthly.html",
                "procesamiento": "Mediana mensual por zona."},
    "nino12_psl": {"nombre": "NOAA PSL, índice Niño 1+2 (ERSST)", "tipo": "indice_climatico", "url": "https://psl.noaa.gov/data/timeseries/month/DS/NINO12/"},
    "oni": {"nombre": "Índice ONI (formato NOAA CPC)", "tipo": "indice_climatico", "url": "https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/ONI_v5.php",
            "nota": "Valor trimestral asignado al mes central del trimestre."},
    "sam_psl": {"nombre": "NOAA PSL, índice AAO/SAM", "tipo": "indice_climatico", "url": "https://psl.noaa.gov/data/climateindices/"},
    "nsidc": {"nombre": "NSIDC Sea Ice Index G02135, extensión diaria (promedio mensual)", "tipo": "satelital", "url": "https://nsidc.org/data/g02135"},
})

zonas = {clave: {"nombre": nombre, "escala": escala, "id_original": zona,
                 "caja": {"lat_min": c[0], "lat_max": c[1], "lon_min": c[2], "lon_max": c[3]},
                 "lat": round((c[0] + c[1]) / 2, 3), "lon": round((c[2] + c[3]) / 2, 3)}
         for clave, (zona, nombre, escala, c) in ZONAS.items()}

ev = pd.read_csv(TAB / "h1d_eventos_pct.csv")
mapa_ev = {"Paita-Sechura": "paita", "Chimbote": "chimbote", "Callao": "callao", "Pisco": "pisco", "Ilo": "ilo"}
eventos = [{"nombre": f"El Niño {r['evento']}",
            "cambio_clorofila_pct": {mapa_ev[k]: round(float(r[k]), 1) for k in mapa_ev}} for _, r in ev.iterrows()]
eventos.append({"nombre": "El Niño 2026 (en curso)", "cambio_clorofila_pct": None,
                "nota": "Niño 1+2 llegó a +3,15 °C en julio de 2026; la clorofila disponible llega hasta enero de 2026."})

asim = pd.read_csv(TAB / "dif_asimetria_temperatura_local.csv")
mapa_z = {v[0]: k for k, v in ZONAS.items()}
hallazgos = [
    {"id": "asimetria", "estado": "comprobado",
     "titulo": "El calor resta fitoplancton; el frío casi no lo devuelve",
     "resultados": {mapa_z[r.zona]: {"pct_por_grado_calido": round(r.pct_por_grado_calido, 1), "pct_por_grado_frio": round(r.pct_por_grado_frio, 1),
                                     "p_asimetria": round(r.p_asimetria, 3)} for r in asim.itertuples()}},
    {"id": "zonas_vulnerables", "estado": "comprobado",
     "titulo": "La costa central es la más vulnerable a El Niño",
     "resumen": "Con Niño 1+2 >= +1 °C la clorofila cae ~45 % en Chimbote y Callao, 20-23 % en Pisco e Ilo y casi nada en Paita-Sechura."},
    {"id": "sin_tendencias", "estado": "comprobado",
     "titulo": "Sin tendencias significativas de clorofila desde 1998"},
    {"id": "antartida", "estado": "comprobado",
     "titulo": "Sin relación robusta entre el océano Austral y el fitoplancton peruano",
     "resumen": "Más de 900 pruebas sin relación significativa tras corrección FDR; controles positivos confirman el método."},
    {"id": "prediccion_2026", "estado": "pendiente",
     "titulo": "Predicción de la caída del fitoplancton durante El Niño 2026"},
]

# BEGIN WEB FINDINGS
actualizaciones_web = {'asimetria': {'titulo': 'Warming and cooling: an observed asymmetry', 'resumen': 'A descriptive pattern, not a better predictor. Out-of-period validation (fit: 1998–2014; test: 2015–2025) changes predictive skill versus a linear model by −1.4% to +1.6%.'}, 'zonas_vulnerables': {'titulo': 'The central coast is most vulnerable to El Niño', 'resumen': 'With Niño 1+2 ≥ +1 °C, chlorophyll falls by about 45% in Chimbote and Callao, 20–23% in Pisco and Ilo, and barely changes in Paita–Sechura.'}, 'sin_tendencias': {'titulo': 'No robust chlorophyll trend since 1998', 'resumen': 'None of the five Peruvian zones has a significant annual chlorophyll trend in 1998–2025. Antarctic warming over 1998–2025 loses significance with a longer record (1986–2025); another product reverses its direction.'}, 'antartida': {'titulo': 'No robust Southern Ocean–Peru relationship', 'resumen': 'More than 1,100 tests found no robust relationship after multiple-testing correction, controlling for El Niño and checking period stability. The apparent 3–4-year lag reflected the El Niño cycle.'}, 'prediccion_2026': {'titulo': 'El Niño 2026: scenario, not a forecast', 'resumen': 'Illustrative scenarios apply historical slopes to assumed El Niño trajectories. They do not predict what will happen in 2026.'}}
for h in hallazgos:
    h.update(actualizaciones_web.get(h["id"], {}))
hallazgos.extend([{'id': 'calentamiento_antartico', 'estado': 'no_robusto', 'titulo': 'Antarctic warming depends on period and product', 'resumen': 'King George Island: CRW gives +0.18 °C/decade (p = 0.002) for 1998–2025, but +0.02 (p = 0.64) for 1986–2025. ERSST gives the opposite direction. A significant result in one window is not robust evidence.'}, {'id': 'rebote_paita', 'estado': 'pendiente', 'titulo': 'A delayed rebound in Paita–Sechura', 'resumen': 'Pending / clue: OC-CCI chlorophyll rises 2–8 months after warming, peaking at 5 months (r = +0.36). MODIS-Aqua keeps the sign but is not significant (r = +0.16 to +0.22; FDR-adjusted p = 0.05–0.13).'}])
# END WEB FINDINGS

salida = {
    "schema_version": "1.1",
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "period": actual["period"],
    "sources": fuentes,
    "notes": actual.get("notes", []) + [
        "Los campos con sufijo _anom_pct o _anom_c son anomalías respecto del promedio del mismo mes (1998-2025).",
        "Las zonas antárticas no tienen clorofila en invierno austral (noche polar): valores null.",
        "Las relaciones entre variables son asociaciones, no pruebas de causalidad.",
    ],
    "metadata": {"variables": variables, "zonas": zonas, "eventos_nino": eventos, "hallazgos": hallazgos},
    "records": records,
}

(OUT / "monitor_data.json").write_text(json.dumps(salida, ensure_ascii=False, indent=1), encoding="utf-8")
(OUT / "monitor-data.js").write_text(
    "// Datos del Monitor ANCHOVETA 360 (formato records + metadata)\nwindow.MONITOR_DATA = "
    + json.dumps(salida, ensure_ascii=False) + ";\n", encoding="utf-8")

campos_nuevos = len(nuevas)
print(f"records: {len(records)} meses ({records[0]['date']} a {records[-1]['date']})")
print(f"campos por mes: {len(records[0])} ({len(records[0]) - campos_nuevos} actuales + {campos_nuevos} nuevos)")
print("último Niño 1+2:", [(r["date"], r["nino12_psl_c"]) for r in records[-3:]])
print("clorofila Chimbote ene-2026:", next(r["chl_chimbote_mg_m3"] for r in records if r["date"] == "2026-01-01"))
