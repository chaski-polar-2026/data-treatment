import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"docs/pruebas_pendientes"))
from config_datos import DATA, ROOT, WEB_EXPORT, require
"""Relacion de cada variable de la cadena fisica con el Nino 1+2 (anomalias mensuales 1998-2025).
Entrada: public/assets/data/el-nino-chain.json de la web. Salida: guias/prompts/datos/nino-relaciones.json
Para cada variable: r a desfase 0, mejor desfase (0-6 meses, Nino adelantado), r sin los anios extremos
(1998, 2016, 2023), n y n efectivo (aprox. Bretherton con autocorrelacion de orden 1), p aproximado.
"""
import json, math
import numpy as np
from scipy import stats

R = require('web/el-nino-chain.json')
OUT = WEB_EXPORT / 'nino-relaciones.json'
d = json.load(open(R, encoding='utf-8'))['records']
d = [r for r in d if r['month'] <= '2025-12']
mes = [r['month'] for r in d]
anio = np.array([int(m[:4]) for m in mes])
nino = np.array([r['nino'] for r in d], float)
VARS = {
    'sst': ('Sea surface temperature', '°C'),
    'seaLevel': ('Sea level', 'm'),
    'deepTemperature': ('Temperature at 100–200 m', '°C'),
    'deepOxygen': ('Oxygen at 100–200 m', 'mmol/m³'),
    'oxygen': ('Surface oxygen', 'mmol/m³'),
    'phosphate': ('Phosphate', 'mmol/m³'),
    'chlorophyll': ('Chlorophyll', 'mg/m³'),
}

def r_con(x, y):
    m = ~(np.isnan(x) | np.isnan(y))
    x, y = x[m], y[m]
    if len(x) < 24: return None, len(x), None
    r = float(np.corrcoef(x, y)[0, 1])
    def ac1(v): return float(np.corrcoef(v[:-1], v[1:])[0, 1])
    rr = ac1(x) * ac1(y)
    neff = max(3.0, len(x) * (1 - rr) / (1 + rr)) if rr < 1 else 3.0
    t = r * math.sqrt((neff - 2) / max(1e-9, 1 - r * r))
    p = float(2 * stats.t.sf(abs(t), neff - 2))
    return r, len(x), (neff, p)

def desplazar(x, k):  # x en t+k alineado con nino en t (el Nino adelanta k meses)
    if k == 0: return nino, x
    return nino[:-k], x[k:]

out = {'source': 'Monthly anomalies, Humboldt box (CMEMS); Niño 1+2 (NOAA PSL). 1998–2025.', 'nota': 'Pearson correlations; p uses an effective sample size that accounts for autocorrelation. Associations, not proof of causation.', 'variables': {}}
extremos = np.isin(anio, [1998, 2016, 2023])
for k, (nombre, unidad) in VARS.items():
    x = np.array([np.nan if r[k] is None else r[k] for r in d], float)
    r0, n0, ex0 = r_con(nino, x)
    mejor = None
    for lag in range(0, 7):
        a, b = desplazar(x, lag)
        r, n, ex = r_con(a, b)
        if r is not None and (mejor is None or abs(r) > abs(mejor[1])): mejor = (lag, r, n, ex)
    xs = x.copy(); xs[extremos] = np.nan
    ns = nino.copy(); ns[extremos] = np.nan
    rs, nsn, exs = r_con(ns, xs)
    out['variables'][k] = {
        'nombre': nombre, 'unidad': unidad,
        'r_lag0': round(r0, 3), 'n': n0, 'neff_lag0': round(ex0[0], 1), 'p_lag0': round(ex0[1], 4),
        'mejor_desfase_meses': mejor[0], 'r_mejor_desfase': round(mejor[1], 3), 'p_mejor_desfase': round(mejor[3][1], 4),
        'r_sin_anios_extremos': None if rs is None else round(rs, 3),
        'signo': 'positive' if r0 > 0 else 'negative',
    }
json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for k, v in out['variables'].items():
    print(k, v['r_lag0'], 'lag', v['mejor_desfase_meses'], v['r_mejor_desfase'], 'sin ext', v['r_sin_anios_extremos'], 'neff', v['neff_lag0'], 'p', v['p_lag0'])
