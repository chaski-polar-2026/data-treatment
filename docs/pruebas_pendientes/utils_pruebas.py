"""Funciones comunes de las pruebas del 14/11/2026 (teleconexion y perspectiva).
Anomalias mensuales, correlacion con n efectivo, correlacion parcial, FDR, consistencia por mitades.
"""
import math
import numpy as np
import pandas as pd
from scipy import stats

EXTREMOS = (1998, 2016, 2023)


def anomalia_mensual(s: pd.Series) -> pd.Series:
    """Quita el ciclo estacional (media de cada mes del calendario)."""
    s = s.astype(float)
    return s - s.groupby(s.index.month).transform('mean')


def _ac1(v: np.ndarray) -> float:
    return float(np.corrcoef(v[:-1], v[1:])[0, 1])


def neff(x: np.ndarray, y: np.ndarray) -> float:
    rr = _ac1(x) * _ac1(y)
    n = len(x)
    return max(3.0, n * (1 - rr) / (1 + rr)) if rr < 1 else 3.0


def corr_neff(x: np.ndarray, y: np.ndarray, min_n: int = 36):
    """Correlacion de Pearson con p basado en n efectivo. Devuelve (r, n, neff, p) o None."""
    m = ~(np.isnan(x) | np.isnan(y))
    x, y = x[m], y[m]
    if len(x) < min_n or np.std(x) == 0 or np.std(y) == 0:
        return None
    r = float(np.corrcoef(x, y)[0, 1])
    ne = neff(x, y)
    t = r * math.sqrt((ne - 2) / max(1e-9, 1 - r * r))
    return r, len(x), ne, float(2 * stats.t.sf(abs(t), ne - 2))


def parcial(x: np.ndarray, y: np.ndarray, z: np.ndarray):
    """Correlacion parcial de x e y controlando z (residuos de regresion lineal). Devuelve (r, n, neff, p) o None."""
    m = ~(np.isnan(x) | np.isnan(y) | np.isnan(z))
    x, y, z = x[m], y[m], z[m]
    if len(x) < 36 or np.std(z) == 0:
        return None

    def res(a):
        b = np.polyfit(z, a, 1)
        return a - np.polyval(b, z)

    return corr_neff(res(x), res(y))


def parcial_multi(x: np.ndarray, y: np.ndarray, Z: np.ndarray):
    """Correlacion parcial de x e y controlando las columnas de Z (residuos por minimos cuadrados). Devuelve (r, n, neff, p) o None."""
    m = ~(np.isnan(x) | np.isnan(y) | np.isnan(Z).any(axis=1))
    x, y, Z = x[m], y[m], Z[m]
    if len(x) < 36:
        return None
    A = np.column_stack([np.ones(len(x)), Z])
    rx = x - A @ np.linalg.lstsq(A, x, rcond=None)[0]
    ry = y - A @ np.linalg.lstsq(A, y, rcond=None)[0]
    return corr_neff(rx, ry)


def fdr(p: np.ndarray) -> np.ndarray:
    """Benjamini-Hochberg."""
    p = np.asarray(p, float)
    o = np.argsort(p)
    m = len(p)
    q = np.empty(m)
    q[o] = np.minimum.accumulate((p[o] * m / (np.arange(m) + 1))[::-1])[::-1]
    return np.minimum(q, 1)


def sin_extremos(s: pd.Series) -> pd.Series:
    return s[~s.index.year.isin(EXTREMOS)]


def mitades(s_idx: pd.DatetimeIndex):
    """Mascaras booleanas de las dos mitades del periodo 1998-2025."""
    a = (s_idx.year >= 1998) & (s_idx.year <= 2011)
    b = (s_idx.year >= 2012) & (s_idx.year <= 2025)
    return a, b


def desplazar(x: pd.Series, k: int) -> pd.Series:
    """x adelantado: el valor de x en t-k alineado con t (x precede a la respuesta k meses)."""
    return x.shift(k)


def mae_rmse(obs: np.ndarray, pred: np.ndarray):
    m = ~(np.isnan(obs) | np.isnan(pred))
    e = obs[m] - pred[m]
    return float(np.mean(np.abs(e))), float(math.sqrt(np.mean(e ** 2))), int(m.sum())


def bootstrap_bloques(err_ref: np.ndarray, err_mod: np.ndarray, anios: np.ndarray, B: int = 2000, seed: int = 7):
    """IC 95 % de la mejora relativa del error absoluto medio (1 - mae_mod/mae_ref), remuestreando anios completos."""
    rng = np.random.default_rng(seed)
    ys = np.unique(anios)
    por = {y: (np.abs(err_ref[anios == y]), np.abs(err_mod[anios == y])) for y in ys}
    vals = []
    for _ in range(B):
        sel = rng.choice(ys, len(ys), replace=True)
        r = np.concatenate([por[y][0] for y in sel]); mo = np.concatenate([por[y][1] for y in sel])
        if np.nanmean(r) > 0:
            vals.append(1 - np.nanmean(mo) / np.nanmean(r))
    return float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))
