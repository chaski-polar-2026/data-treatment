from config_datos import DATA, OUTPUT, TABLES, require
"""Bloque 1 (preregistro 14/11/2026): senales antarticas y del Pacifico sur frente a la costa peruana.
Correr: PYTHONIOENCODING=utf-8 python bloque1_teleconexion.py   (sin -I). Ajustar R_DATA si cambia la ruta.
Control de El Nino: correlacion parcial controlando el Nino 1+2 del instante del objetivo y del instante del predictor.
"""
import json, sys
from pathlib import Path
import numpy as np, pandas as pd
sys.path.insert(0, str(Path(__file__).parent))
from utils_pruebas import anomalia_mensual, corr_neff, parcial_multi, fdr, EXTREMOS

R_DATA = str(DATA) + '/'
REPO = OUTPUT
LAGS = (0, 1, 2, 3, 6, 9, 12)
ZONAS = ['paita', 'chimbote', 'callao', 'pisco', 'ilo']


def cargar():
    mon = pd.DataFrame(json.load(open(require('pruebas/json_pagina/monitor_data.json'), encoding='utf-8'))['records'])
    mon['date'] = pd.to_datetime(mon['date']); mon = mon.set_index('date')
    pan = pd.read_csv(require('drive_aaron/connectivity_panel_monthly.csv'), parse_dates=['date'])
    rng = pd.date_range('1998-01-01', '2025-12-01', freq='MS')
    return mon.reindex(rng), pan, rng


def pn(pan, rng, region, banda, col):
    q = pan[(pan.region == region) & (pan.depth_band == banda)].set_index('date')[col].sort_index()
    return q.reindex(rng)


def predictores(mon, pan, rng):
    P = {'SAM': mon['sam_index'], 'Antarctic sea ice anomaly': mon['sea_ice_antarctic_anom_mkm2'],
         'SST Rey Jorge': mon['sst_rey_jorge_anom_c'], 'SST Antarctic Peninsula (monitor)': mon['sst_peninsula_antartica_anom_c']}
    for reg in ('bellingshausen', 'peninsula_antarctica', 'south_pacific_intermediate', 'south_pacific_subtropical'):
        P[f'Temp 0-5 m {reg}'] = pn(pan, rng, reg, 'surface_0_5m', 'thetao_anom')
    return P


def objetivos(mon, pan, rng):
    T = {}
    for z in ZONAS:
        T[f'SST {z}'] = mon[f'sst_{z}_anom_c']; T[f'Chlorophyll {z}'] = mon[f'chl_{z}_anom_pct']
    T['Humboldt temp 100-200 m'] = pn(pan, rng, 'peru_humboldt', 'subsurface_100_200m', 'thetao_anom')
    T['Humboldt oxygen 100-200 m'] = pn(pan, rng, 'peru_humboldt', 'subsurface_100_200m', 'o2_anom')
    T['Humboldt nitrate 0-5 m'] = pn(pan, rng, 'peru_humboldt', 'surface_0_5m', 'no3_anom')
    T['Humboldt chlorophyll 0-5 m'] = pn(pan, rng, 'peru_humboldt', 'surface_0_5m', 'chl_anom')
    T['Transition temp 0-5 m'] = pn(pan, rng, 'transition_humboldt', 'surface_0_5m', 'thetao_anom')
    T['Transition chlorophyll 0-5 m'] = pn(pan, rng, 'transition_humboldt', 'surface_0_5m', 'chl_anom')
    return T


def correr_familia(P, T, nino, lags=LAGS):
    """Devuelve DataFrame con una fila por prueba (predictor, objetivo, retraso)."""
    idx = nino.index
    n12 = anomalia_mensual(nino).values
    filas = []
    for pnom, p in P.items():
        pa = anomalia_mensual(p.reindex(idx))
        for tnom, t in T.items():
            ta = anomalia_mensual(t.reindex(idx)).values
            for k in lags:
                x = pa.shift(k).values
                raw = corr_neff(x, ta)
                Z = np.column_stack([n12, pd.Series(n12).shift(k).values])
                par = parcial_multi(x, ta, Z)
                if raw is None or par is None:
                    continue
                filas.append(dict(predictor=pnom, objetivo=tnom, retraso_meses=k, n=raw[1], neff=round(raw[2], 1),
                                  r_cruda=raw[0], p_cruda=raw[3], r_parcial=par[0], p_parcial=par[3]))
    df = pd.DataFrame(filas)
    df['q_cruda'] = fdr(df.p_cruda.values); df['q_parcial'] = fdr(df.p_parcial.values)
    return df, idx, n12


def comprobar(df, P, T, idx, n12):
    """Para las pruebas con q_parcial < 0,05: mitades, sin extremos y signo."""
    ext = idx.year.isin(EXTREMOS)
    h1 = (idx.year <= 2011)
    out = []
    for _, f in df[df.q_parcial < .05].iterrows():
        k = int(f.retraso_meses)
        x = anomalia_mensual(P[f.predictor].reindex(idx)).shift(k).values
        y = anomalia_mensual(T[f.objetivo].reindex(idx)).values
        Z = np.column_stack([n12, pd.Series(n12).shift(k).values])

        def pr(mask):
            r = parcial_multi(np.where(mask, x, np.nan), np.where(mask, y, np.nan), Z)
            return None if r is None else (r[0], r[3])

        a, b, c = pr(h1), pr(~h1), pr(~ext)
        out.append(dict(predictor=f.predictor, objetivo=f.objetivo, retraso_meses=k, r_parcial=f.r_parcial, q_parcial=f.q_parcial,
                        r_mitad1=None if a is None else a[0], r_mitad2=None if b is None else b[0],
                        r_sin_extremos=None if c is None else c[0], p_sin_extremos=None if c is None else c[1]))
    o = pd.DataFrame(out)
    if len(o):
        o['mismo_signo_mitades'] = np.sign(o.r_mitad1) == np.sign(o.r_mitad2)
        o['hallazgo'] = o.mismo_signo_mitades & (o.p_sin_extremos < .05)
    return o


if __name__ == '__main__':
    mon, pan, rng = cargar()
    P, T = predictores(mon, pan, rng), objetivos(mon, pan, rng)
    nino = mon['nino12_psl_c']
    df, idx, n12 = correr_familia(P, T, nino)
    df.round(5).to_csv(REPO / 'data/tablas_pruebas_pendientes/bloque1_teleconexion.csv', index=False, encoding='utf-8')
    comp = comprobar(df, P, T, idx, n12)
    comp.round(5).to_csv(REPO / 'data/tablas_pruebas_pendientes/bloque1_teleconexion_supervivientes.csv', index=False, encoding='utf-8')
    print('pruebas:', len(df), '(esperadas 896; el resto se descartó por datos insuficientes)')
    print('p cruda <0,05:', int((df.p_cruda < .05).sum()), '| q cruda <0,05:', int((df.q_cruda < .05).sum()),
          '| q parcial <0,05:', int((df.q_parcial < .05).sum()))
    perd = df[(df.q_cruda < .05) & (df.q_parcial >= .05)]
    print('con q cruda<0,05 que dejan de serlo al controlar El Nino:', len(perd), 'de', int((df.q_cruda < .05).sum()))
    print('mediana |r| cruda %.3f, parcial %.3f' % (df.r_cruda.abs().median(), df.r_parcial.abs().median()))
    if len(comp):
        print('supervivientes (q parcial<0,05):', len(comp), '| hallazgos completos:', int(comp.hallazgo.sum()))
        print(comp.sort_values('q_parcial').head(10).round(3).to_string(index=False))
    print(df.sort_values('p_parcial').head(8)[['predictor', 'objetivo', 'retraso_meses', 'r_cruda', 'r_parcial', 'p_parcial', 'q_parcial']].round(3).to_string(index=False))
