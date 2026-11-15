import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"docs/pruebas_pendientes"))
from config_datos import DATA, ROOT, WEB_EXPORT, require
"""Exporta las series de la ronda de seis variables a JSON para el panel de tendencias de la web,
y una tabla de referencia con el mismo calculo que usa la web (media anual de valores crudos, >=6 meses,
anios <= 2025, pendiente de Sen y Mann-Kendall con aproximacion normal y correccion por empates).
Correr: PYTHONIOENCODING=utf-8 python exportar_ronda_json.py
"""
import json, math
from collections import defaultdict
import numpy as np, pandas as pd
import xarray as xr

R = str(DATA) + '/'
OUT = str(WEB_EXPORT) + '/'
ANIO_FINAL = 2025

pan = pd.read_csv(R + 'drive_aaron/connectivity_panel_monthly.csv', parse_dates=['date'])
def panel(band, col):
    q = pan[(pan.region == 'peru_humboldt') & (pan.depth_band == band)].set_index('date')[col].sort_index()
    return q

def lista(s, inicio, fin):
    idx = pd.period_range(inicio, fin, freq='M')
    s = s.copy(); s.index = s.index.to_period('M'); s = s[~s.index.duplicated()]
    return [None if pd.isna(v) else round(float(v), 4) for v in s.reindex(idx)]

series = {}
t = panel('subsurface_100_200m', 'thetao')
series['temp100'] = dict(nombre='Temperature at 100–200 m (Humboldt region)', unidad='°C', alcance='Humboldt region (Peru coast)',
    tipo='reanalysis', fuente='Copernicus Marine physics reanalysis (GLORYS12), mean of 100–200 m over the Humboldt box',
    inicio='1998-01', valores=lista(t, '1998-01', '2025-12'))
z = panel('surface_2d', 'zos')
series['sealevel'] = dict(nombre='Sea level anomaly (Humboldt region)', unidad='m', alcance='Humboldt region (Peru coast)',
    tipo='reanalysis', fuente='Copernicus Marine physics reanalysis (GLORYS12), sea surface height over the Humboldt box',
    inicio='1998-01', valores=lista(z, '1998-01', '2025-12'))
o = panel('subsurface_100_200m', 'o2')
series['oxy100'] = dict(nombre='Dissolved oxygen at 100–200 m (Humboldt region)', unidad='mmol/m³', alcance='Humboldt region (Peru coast)',
    tipo='reanalysis', fuente='Copernicus Marine biogeochemistry reanalysis, mean of 100–200 m over the Humboldt box',
    inicio='1998-01', valores=lista(o, '1998-01', '2025-12'))

fr = []
for m in range(1, 13):
    d = pd.read_csv(R + f'datos/pesquerias/hielo_antartico_nsidc/S_{m:02d}.csv', skipinitialspace=True)
    d.columns = [c.strip() for c in d.columns]
    d = d[d.extent > 0]
    fr.append(pd.Series(d.extent.values, index=pd.to_datetime(dict(year=d.year, month=d.mo, day=1))))
hielo = pd.concat(fr).sort_index()
series['seaice'] = dict(nombre='Antarctic sea-ice extent', unidad='million km²', alcance='Antarctica (whole Southern Ocean)',
    tipo='observation', fuente='NSIDC Sea Ice Index (G02135), monthly extent',
    inicio='1979-01', valores=lista(hielo, '1979-01', '2025-12'))

ds = xr.open_dataset(require('datos/tendencias_largas/ersstv5_sst_mnmean.nc'))
sst = ds['sst']
zonas = {'norte_centro': (-10, 0, 270, 280), 'costa_sur': (-18, -10, 280, 290)}
zl = {}
for nom, (la, lb, lo1, lo2) in zonas.items():
    b = sst.sel(lat=slice(lb, la), lon=slice(lo1, lo2)).mean(['lat', 'lon'])
    s = pd.Series(b.values.astype(float), index=pd.to_datetime(b.time.values))
    s = s[s.index >= '1900-01-01']
    zl[nom] = lista(s, '1900-01', '2025-12')
series['sst_long'] = dict(nombre='Sea surface temperature, long record (ERSST)', unidad='°C',
    alcance='Peru coast: north-central box (0–10°S, 90–80°W) and south box (10–18°S, 80–70°W)',
    tipo='observation-based reconstruction', fuente='NOAA Extended Reconstructed SST v5 (ERSST v5), 2° grid',
    inicio='1900-01', zonas=zl)

os_ = {'generado': 'ronda de seis variables (14/11/2026); ver data-treatment docs/pruebas_pendientes/RESULTADOS_RONDA_SEIS_VARIABLES.md',
       'series': series}
import os
os.makedirs(OUT, exist_ok=True)
json.dump(os_, open(OUT + 'tendencias-ronda.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))

# Referencia: calculo igual al de la web
def anuales(vals, inicio):
    a, m = int(inicio[:4]), int(inicio[5:7]); por = defaultdict(list)
    for v in vals:
        if v is not None: por[a].append(v)
        m += 1
        if m > 12: m = 1; a += 1
    return [(x, float(np.mean(l))) for x, l in sorted(por.items()) if len(l) >= 6 and x <= ANIO_FINAL]

def mk(pts):
    n = len(pts)
    x = np.array([p[0] for p in pts], float); y = np.array([p[1] for p in pts])
    sl = [(y[j] - y[i]) / (x[j] - x[i]) for i in range(n) for j in range(i + 1, n)]
    S = sum(np.sign(y[j] - y[i]) for i in range(n) for j in range(i + 1, n))
    _, c = np.unique(y, return_counts=True)
    var = (n * (n - 1) * (2 * n + 5) - sum(k * (k - 1) * (2 * k + 5) for k in c)) / 18
    z = (S - np.sign(S)) / math.sqrt(var) if S != 0 else 0.0
    p = math.erfc(abs(z) / math.sqrt(2))
    return float(np.median(sl)), p, n

filas = []
def ref(nombre, vals, inicio):
    pts = anuales(vals, inicio)
    for ini in (1998, 2003, 2010, 1979, 1950, 1900):
        if ini < pts[0][0] and ini != 1998: continue
        sub = [p for p in pts if p[0] >= max(ini, pts[0][0])]
        if len(sub) < 8: continue
        sen, p, n = mk(sub)
        filas.append(dict(variable=nombre, desde=sub[0][0], hasta=sub[-1][0], n=n, sen_por_decada=round(sen * 10, 4), p=round(p, 4)))
for k, v in series.items():
    if 'valores' in v: ref(k, v['valores'], v['inicio'])
    else:
        for zn, vals in v['zonas'].items(): ref(f'{k}:{zn}', vals, v['inicio'])
df = pd.DataFrame(filas)
df.to_csv(OUT + 'referencia_tendencias_web.csv', index=False)
print(df.to_string())
print(os.path.getsize(OUT + 'tendencias-ronda.json') // 1024, 'KB')
