"""Antartida y paises vecinos (Chile, Argentina): capturas anuales FAO vs senales antarticas.
Pares fijados de antemano; periodo 1998-2024 (n=27). Para cada par: r en niveles, r en primeras diferencias
(quita tendencias compartidas), r tras quitar tendencia lineal, r parcial controlando Nino 1+2, p con n efectivo
(autocorrelacion de orden 1) y FDR (Benjamini-Hochberg) sobre todas las pruebas de diferencias.
Las capturas no son abundancia: las afectan cuotas, esfuerzo y colapsos por sobrepesca.
"""
import json, math
import numpy as np, pandas as pd
from scipy import stats

R = 'D:/hackathon/NASA/'
fao = pd.read_csv(R + 'datos/pesquerias/fao_series.csv', encoding='utf-8')
fao.columns = [c.strip() for c in fao.columns]
fao['especie'] = fao['especie'].str.replace('\ufffd', '?')
mon = pd.DataFrame(json.load(open(R + 'pruebas/json_pagina/monitor_data.json', encoding='utf-8'))['records'])
mon['date'] = pd.to_datetime(mon['date']); mon = mon.set_index('date')
Y = list(range(1998, 2025))

def anual(col, meses=None):
    s = mon[col].astype(float)
    if meses: s = s[s.index.month.isin(meses)]
    g = s.groupby(s.index.year)
    out = g.mean()[g.count() >= (2 if meses else 9)]
    return out.reindex(Y)

# hielo: extension NSIDC (media anual)
fr = []
for m in range(1, 13):
    d = pd.read_csv(R + f'datos/pesquerias/hielo_antartico_nsidc/S_{m:02d}.csv', skipinitialspace=True)
    d.columns = [c.strip() for c in d.columns]; d = d[d.extent > 0]
    fr.append(pd.Series(d.extent.values, index=pd.to_datetime(dict(year=d.year, month=d.mo, day=1))))
hielo = pd.concat(fr).sort_index(); hielo = hielo.groupby(hielo.index.year).mean().reindex(Y)

F = {
    'Sea ice extent (annual)': hielo,
    'SAM index (annual)': anual('sam_index'),
    'Rey Jorge chlorophyll (Dec-Mar)': anual('chl_rey_jorge_mg_m3', [12, 1, 2, 3]),
}
nino = anual('nino12_psl_c')

PARES = [('Chile', 'Jurel'), ('Chile', 'Anchoveta'), ('Chile', 'Sardina'), ('Chile', 'Sardina araucana'),
         ('Chile', 'Merluza del Pacífico sur'), ('Chile', 'Pota (jibia)'),
         ('Argentina', 'Calamar argentino'), ('Argentina', 'Merluza argentina')]

def serie(pais, esp):
    d = fao[(fao.pais == pais) & (fao.especie == esp) & (fao.tipo == 'pesca')].groupby('anio').toneladas.sum()
    return d.reindex(Y)

def neff(x, y):
    def ac(v): return float(np.corrcoef(v[:-1], v[1:])[0, 1])
    rr = ac(x) * ac(y)
    return max(3.0, len(x) * (1 - rr) / (1 + rr)) if rr < 1 else 3.0

def corr(x, y):
    m = ~(np.isnan(x) | np.isnan(y)); x, y = x[m], y[m]
    if len(x) < 12: return None
    r = float(np.corrcoef(x, y)[0, 1]); ne = neff(x, y)
    t = r * math.sqrt((ne - 2) / max(1e-9, 1 - r * r))
    return r, len(x), float(2 * stats.t.sf(abs(t), ne - 2))

def detr(v):
    m = ~np.isnan(v); x = np.arange(len(v))
    b = np.polyfit(x[m], v[m], 1); out = v - np.polyval(b, x); return out

def parcial(x, y, z):
    m = ~(np.isnan(x) | np.isnan(y) | np.isnan(z)); x, y, z = x[m], y[m], z[m]
    def res(a):
        b = np.polyfit(z, a, 1); return a - np.polyval(b, z)
    return float(np.corrcoef(res(x), res(y))[0, 1])

filas = []
for pais, esp in PARES:
    c = np.log(serie(pais, esp).replace(0, np.nan).values.astype(float))
    for fn, f in F.items():
        fv = f.values.astype(float)
        for lag in (0, 1):
            cc = c[lag:]; ff = fv[:len(fv) - lag] if lag else fv
            nn = nino.values.astype(float)[:len(nino) - lag] if lag else nino.values.astype(float)
            niv = corr(ff, cc)
            dif = corr(np.diff(ff), np.diff(cc))
            det = corr(detr(ff), detr(cc))
            if niv is None or dif is None or det is None: continue
            pr = parcial(np.diff(ff), np.diff(cc), np.diff(nn)) if len(nn) == len(ff) else None
            filas.append(dict(pais=pais, especie=esp, forzante=fn, lag_anios=lag, n=niv[1],
                              r_niveles=niv[0], p_niveles=niv[2], r_dif=dif[0], p_dif=dif[2], r_sin_tendencia=det[0], p_sin_tendencia=det[2], r_dif_control_nino=pr))
df = pd.DataFrame(filas)
p = df.p_dif.values; o = np.argsort(p); m = len(p)
q = np.empty(m); q[o] = np.minimum.accumulate((p[o] * m / (np.arange(m) + 1))[::-1])[::-1]
df['q_fdr_dif'] = np.minimum(q, 1)
df.round(4).to_csv(R + 'pruebas/fitoplancton/tablas/antartida_vecinos.csv', index=False, encoding='utf-8')
pd.set_option('display.width', 250); pd.set_option('display.max_rows', 200)
print('pruebas:', len(df), '| p<0.05 en diferencias:', int((df.p_dif < .05).sum()), '| q<0.05:', int((df.q_fdr_dif < .05).sum()))
print(df.sort_values('p_niveles').head(8)[['pais', 'especie', 'forzante', 'lag_anios', 'n', 'r_niveles', 'p_niveles', 'r_dif', 'p_dif', 'r_sin_tendencia', 'p_sin_tendencia', 'q_fdr_dif']].round(3).to_string(index=False))
print('--- mejores en diferencias')
print(df.sort_values('p_dif').head(6)[['pais', 'especie', 'forzante', 'lag_anios', 'r_niveles', 'r_dif', 'p_dif', 'q_fdr_dif']].round(3).to_string(index=False))
