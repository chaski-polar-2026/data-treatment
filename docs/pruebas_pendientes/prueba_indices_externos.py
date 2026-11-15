"""Bloque 2 (preregistro 14/11/2026): indices externos (PSA, presion del Mar de Amundsen, altura geopotencial).
No existen en disco. Este script queda listo para cuando se coloque un CSV con columnas: fecha, indice, valor
(una fila por mes e indice; fecha como AAAA-MM o AAAA-MM-01). Aplica la misma familia y el mismo control que el bloque 1
(corr. parcial controlando el Nino 1+2) frente a los 16 objetivos peruanos, retrasos 0-12 meses.
Uso:  python prueba_indices_externos.py ruta.csv     |     python prueba_indices_externos.py --selftest
Datos faltantes (por verificar): indices PSA1/PSA2 mensuales; indice del Amundsen Sea Low; altura geopotencial 500 hPa. Periodo 1998-2025.
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd
sys.path.insert(0, str(Path(__file__).parent))
from bloque1_teleconexion import cargar, objetivos, correr_familia, comprobar, REPO


def leer_indices(ruta, rng):
    d = pd.read_csv(ruta)
    assert {'fecha', 'indice', 'valor'} <= set(d.columns), 'El CSV necesita las columnas fecha, indice y valor'
    d['fecha'] = pd.to_datetime(d['fecha']).dt.to_period('M').dt.to_timestamp()
    return {k: g.set_index('fecha')['valor'].astype(float).reindex(rng) for k, g in d.groupby('indice')}


def selftest():
    rng = pd.date_range('1998-01-01', '2025-12-01', freq='MS')
    g = np.random.default_rng(3)
    x = pd.Series(g.normal(size=len(rng)), index=rng)
    y = 0.6 * x.shift(2).fillna(0) + g.normal(size=len(rng)) * 0.8
    nino = pd.Series(g.normal(size=len(rng)), index=rng)
    df, idx, n12 = correr_familia({'sintetico': x}, {'objetivo': y}, nino, lags=(0, 1, 2, 3, 6))
    f2 = df[df.retraso_meses == 2].iloc[0]
    assert 0.35 < f2.r_parcial < 0.7 and f2.q_parcial < 0.05, f2
    assert (df[df.retraso_meses != 2].q_parcial > 0.05).all(), df
    print('selftest OK: r parcial a 2 meses = %.2f (esperado ~0,5), otros retrasos sin senal' % f2.r_parcial)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--selftest':
        selftest(); sys.exit(0)
    if len(sys.argv) < 2 or not Path(sys.argv[1]).exists():
        print('No hay archivo de indices externos. Coloca un CSV (fecha, indice, valor) y vuelve a ejecutar. Ver la lista de datos faltantes en este script.')
        sys.exit(0)
    mon, pan, rng = cargar()
    P = leer_indices(sys.argv[1], rng)
    T = objetivos(mon, pan, rng)
    df, idx, n12 = correr_familia(P, T, mon['nino12_psl_c'])
    out = REPO / 'data/tablas_pruebas_pendientes/bloque2_indices_externos.csv'
    df.round(5).to_csv(out, index=False, encoding='utf-8')
    comp = comprobar(df, P, T, idx, n12)
    print('pruebas:', len(df), '| q parcial<0,05:', int((df.q_parcial < .05).sum()), '| hallazgos completos:', int(comp.hallazgo.sum()) if len(comp) else 0)
