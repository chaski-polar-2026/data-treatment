"""Bloque 4 (preregistro 14/11/2026): desembarques mensuales de anchoveta (BCRP 2003-2026) frente a climatologia y Nino 1+2.
Objetivo: log(1 + total_t). Origen movil 2010-2025, horizontes 1 y 3 meses. Modelos: climatologia mensual frente a
climatologia + Nino 1+2 con rezago fijo L (1, 2 o 3 meses; solo es utilizable si L >= horizonte).
Variante: sin 2016, 2017 y 2023 en el entrenamiento. Metricas en todos los meses y en los meses con desembarque.
Correr: PYTHONIOENCODING=utf-8 python bloque4_desembarques.py
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd
sys.path.insert(0, str(Path(__file__).parent))
from utils_pruebas import bootstrap_bloques
from bloque1_teleconexion import cargar, REPO

CSV = REPO / 'data/punto1_anchoveta/1a_desembarques_mensuales_bcrp/desembarques_anchoveta_mensual_2003_2026.csv'
INICIO = pd.Timestamp('2010-01-01')
FIN = pd.Timestamp('2025-12-01')


def pronosticar(y: pd.Series, nino: pd.Series, h: int, lag: int, sin_extremos: bool):
    idx = y.index
    filas = []
    for t_i, t in enumerate(idx):
        o_i = t_i - h
        if t < INICIO or t > FIN or o_i < 36 or lag < h:
            continue
        train = y.iloc[:o_i + 1].copy()
        if sin_extremos:
            train[train.index.year.isin([2016, 2017, 2023])] = np.nan
        clim = train.groupby(train.index.month).mean()
        cl = train.index.month.map(clim).values
        res = train.values - cl
        nn = nino.shift(lag).iloc[:o_i + 1].values
        m = ~(np.isnan(res) | np.isnan(nn))
        if m.sum() < 36:
            continue
        b = float(nn[m] @ res[m] / (nn[m] @ nn[m]))
        nt = nino.shift(lag).iloc[t_i]
        cl_t = clim.get(t.month, np.nan)
        if np.isnan(nt) or np.isnan(cl_t) or np.isnan(y.iloc[t_i]):
            continue
        filas.append(dict(t=t, anio=t.year, obs=y.iloc[t_i], clim=cl_t, nino=cl_t + b * nt))
    return pd.DataFrame(filas)


def metricas(df):
    e_ref, e_mod = (df.obs - df.clim).values, (df.obs - df.nino).values
    lo, hi = bootstrap_bloques(e_ref, e_mod, df.anio.values)
    return dict(n=len(df), mae_clim=np.mean(np.abs(e_ref)), mae_nino=np.mean(np.abs(e_mod)),
                mejora=1 - np.mean(np.abs(e_mod)) / np.mean(np.abs(e_ref)), ic_inf=lo, ic_sup=hi,
                rmse_mejora=1 - np.sqrt(np.mean(e_mod ** 2)) / np.sqrt(np.mean(e_ref ** 2)))


if __name__ == '__main__':
    d = pd.read_csv(CSV)
    d['mes'] = pd.to_datetime(d['mes'])
    total = d.set_index('mes')['total_t'].astype(float)
    mon, pan, rng = cargar()
    rng2 = pd.date_range('2003-01-01', '2025-12-01', freq='MS')
    y = np.log1p(total.reindex(rng2))
    nino = mon['nino12_psl_c'].reindex(rng2)
    print('meses con desembarque cero (vedas):', int((total.reindex(rng2) == 0).sum()), 'de', len(rng2))
    filas = []
    for h in (1, 3):
        for lag in (1, 2, 3):
            if lag < h:
                continue
            for var in (False, True):
                p = pronosticar(y, nino, h, lag, var)
                for sub, dd in (('todos los meses', p), ('meses con desembarque', p[p.obs > np.log1p(0)])):
                    filas.append(dict(horizonte_meses=h, rezago_nino=lag, sin_2016_2017_2023_en_entrenamiento=var, meses=sub, **metricas(dd)))
    df = pd.DataFrame(filas)
    df['mejora_clara'] = df.ic_inf > 0
    df.round(4).to_csv(REPO / 'data/tablas_pruebas_pendientes/bloque4_desembarques.csv', index=False, encoding='utf-8')
    pd.set_option('display.width', 220)
    print(df[['horizonte_meses', 'rezago_nino', 'sin_2016_2017_2023_en_entrenamiento', 'meses', 'n', 'mejora', 'ic_inf', 'ic_sup', 'mejora_clara']].round(3).to_string(index=False))
