"""Bloque 3 (preregistro 14/11/2026): perspectiva retrospectiva de TSM y clorofila (log) a 1, 2 y 3 meses.
Origen movil: para pronosticar el mes t con horizonte h solo se usan datos hasta t-h. Orígenes de 2010-01 a 2025-12.
Modelos: climatologia, persistencia, persistencia amortiguada y regresion sobre anomalia actual y Nino 1+2 actual.
Salida: data/tablas_pruebas_pendientes/bloque3_perspectiva.csv y data/perspectiva_acierto.json.
Correr: PYTHONIOENCODING=utf-8 python bloque3_perspectiva.py
"""
import json, sys
from pathlib import Path
import numpy as np, pandas as pd
sys.path.insert(0, str(Path(__file__).parent))
from utils_pruebas import bootstrap_bloques
from bloque1_teleconexion import cargar, ZONAS, REPO

HORIZONTES = (1, 2, 3)
INICIO = pd.Timestamp('2010-01-01')


def pronosticar(serie: pd.Series, nino: pd.Series, h: int, sin1998: bool = False) -> pd.DataFrame:
    idx = serie.index
    filas = []
    for t_i, t in enumerate(idx):
        o_i = t_i - h
        if t < INICIO or o_i < 36:
            continue
        train = serie.iloc[:o_i + 1].copy()
        nin = nino.iloc[:o_i + 1].values.copy()
        if sin1998:
            train[train.index.year == 1998] = np.nan
        clim = train.groupby(train.index.month).mean()
        cl = train.index.month.map(clim).values
        an = (train.values - cl)
        an_o = an[-1]
        cl_t = clim.get(t.month, np.nan)
        obs = serie.iloc[t_i]
        if np.isnan(obs) or np.isnan(an_o) or np.isnan(cl_t) or np.isnan(nin[-1]):
            continue
        xs, ys, ns = an[:-h], an[h:], nin[:-h]
        m = ~(np.isnan(xs) | np.isnan(ys) | np.isnan(ns))
        if m.sum() < 36:
            continue
        phi = float(xs[m] @ ys[m] / (xs[m] @ xs[m]))
        A = np.column_stack([xs[m], ns[m]])
        b = np.linalg.lstsq(A, ys[m], rcond=None)[0]
        filas.append(dict(t=t, anio=t.year, obs=obs, clim=cl_t, pers=cl_t + an_o, amort=cl_t + phi * an_o,
                          nino=cl_t + b[0] * an_o + b[1] * nin[-1]))
    return pd.DataFrame(filas)


def resumen(df: pd.DataFrame, modelo: str):
    e_ref = (df.obs - df.clim).values
    e_mod = (df.obs - df[modelo]).values
    mae_ref, mae_mod = np.mean(np.abs(e_ref)), np.mean(np.abs(e_mod))
    lo, hi = bootstrap_bloques(e_ref, e_mod, df.anio.values)
    an_obs = df.obs - df.clim
    hit = float(np.mean(np.sign(df[modelo] - df.clim) == np.sign(an_obs)))
    return dict(n=len(df), mae_clim=mae_ref, mae_modelo=mae_mod, mejora=1 - mae_mod / mae_ref, ic_inf=lo, ic_sup=hi,
                rmse_mejora=1 - np.sqrt(np.mean(e_mod ** 2)) / np.sqrt(np.mean(e_ref ** 2)), acierto_signo=hit,
                tasa_base_positivo=float(np.mean(an_obs > 0)))


if __name__ == '__main__':
    mon, pan, rng = cargar()
    nino = mon['nino12_psl_c']
    series = {}
    for z in ZONAS:
        series[('SST', z)] = mon[f'sst_{z}_c']
        series[('Chlorophyll (log)', z)] = np.log(mon[f'chl_{z}_mg_m3'].where(mon[f'chl_{z}_mg_m3'] > 0))
    filas = []
    for (var, z), s in series.items():
        for h in HORIZONTES:
            base = {v: pronosticar(s, nino, h, sin1998=v) for v in (False, True)}
            for modelo in ('pers', 'amort', 'nino'):
                r0 = resumen(base[False], modelo)
                r1 = resumen(base[True], modelo)
                filas.append(dict(variable=var, zona=z, horizonte_meses=h, modelo=modelo, **r0,
                                  mejora_sin1998=r1['mejora'], ic_inf_sin1998=r1['ic_inf'], ic_sup_sin1998=r1['ic_sup']))
    df = pd.DataFrame(filas)
    df['mejora_clara'] = (df.ic_inf > 0) & (df.ic_inf_sin1998 > 0)
    df.round(4).to_csv(REPO / 'data/tablas_pruebas_pendientes/bloque3_perspectiva.csv', index=False, encoding='utf-8')
    pd.set_option('display.width', 220)
    print('combinaciones:', len(df), '| con mejora clara (IC > 0 con y sin 1998):', int(df.mejora_clara.sum()))
    res = df.groupby(['variable', 'horizonte_meses', 'modelo']).agg(mejora_mediana=('mejora', 'median'), zonas_claras=('mejora_clara', 'sum'), acierto_signo=('acierto_signo', 'median'), base=('tasa_base_positivo', 'median'))
    print(res.round(3).to_string())
    out = {'source': 'Retrospective monthly hindcast 2010-2025, local data (OC-CCI chlorophyll, NOAA CRW SST, Niño 1+2 NOAA PSL).',
           'warning': 'Monthly data only. Skill is measured on past months; it does not guarantee future accuracy. Not a forecast of fish.',
           'results': [dict(variable=r.variable, zone=r.zona, horizon_months=int(r.horizonte_meses), model=r.modelo,
                            mae_improvement=round(r.mejora, 4), ci95=[round(r.ic_inf, 4), round(r.ic_sup, 4)],
                            mae_improvement_without_1998=round(r.mejora_sin1998, 4), sign_hit_rate=round(r.acierto_signo, 3),
                            base_rate_positive=round(r.tasa_base_positivo, 3), n=int(r.n),
                            status='clear improvement over climatology' if r.mejora_clara else 'no clear improvement over climatology')
                       for r in df.itertuples()]}
    json.dump(out, open(REPO / 'data/perspectiva_acierto.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
