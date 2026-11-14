"""Compara altimetría mensual y GLORYS usando el método de la ronda previa."""
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests
import xarray as xr
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
EXTREMES = {1998, 2016, 2023}


def annual(s):
    s = s.dropna()
    anomalies = s - s.groupby(s.index.month).transform('mean')
    grouped = anomalies.groupby(anomalies.index.year)
    return grouped.mean()[grouped.count() >= 9]


def trend(y):
    x = y.index.to_numpy(dtype=float); v = y.to_numpy(dtype=float); n = len(v)
    if n < 8: return None
    tau, p = stats.kendalltau(x, v)
    slopes = np.sort([(v[j]-v[i])/(x[j]-x[i]) for i in range(n) for j in range(i+1,n)])
    count=len(slopes); c=1.96*np.sqrt(n*(n-1)*(2*n+5)/18)
    lo=int(max(0,np.floor((count-c)/2))); hi=int(min(count-1,np.ceil((count+c)/2)))
    return {'n': n, 'tau': tau, 'p': p, 'sen_cm_decada': float(np.median(slopes)*1000),
            'ic_inf_cm_decada': float(slopes[lo]*1000), 'ic_sup_cm_decada': float(slopes[hi]*1000)}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input', type=Path, default=Path('/tmp/anchoveta_altimetria/sla_peru_1993_2025.nc'))
    p.add_argument('--panel', type=Path, default=ROOT/'data/processed/tables/connectivity_panel_monthly.csv')
    p.add_argument('--output', type=Path, default=ROOT/'data/tablas_pruebas_pendientes/altimetria')
    p.add_argument('--report', type=Path, default=ROOT/'docs/pruebas_pendientes/RESULTADOS_ALTIMETRIA.md')
    a=p.parse_args()
    with xr.open_dataset(a.input) as ds:
        if 'sla' not in ds: raise SystemExit('El archivo no contiene sla.')
        v=ds.sla
        lat=next((k for k in ('latitude','lat') if k in v.dims),None)
        lon=next((k for k in ('longitude','lon') if k in v.dims),None)
        if not lat or not lon or 'time' not in v.dims: raise SystemExit('Faltan dimensiones espaciales o temporales.')
        if v.attrs.get('units') not in ('m','meter','metre','meters','metres'): raise SystemExit('Unidades de SLA no reconocidas como metros.')
        v=v.assign_coords({lon:((v[lon]+180)%360)-180}).sortby(lon).sortby(lat)
        v=v.sel({lon:slice(-85,-70),lat:slice(-18.35,-3.38), 'time':slice('1993-01-01','2025-12-31')})
        if not v.sizes.get(lat) or not v.sizes.get(lon): raise SystemExit('La caja no contiene celdas.')
        spatial_median=v.median((lat,lon),skipna=True).to_series()
        spatial_mean=v.weighted(np.cos(np.deg2rad(v[lat]))).mean((lat,lon),skipna=True).to_series()
        coverage=v.notnull().sum((lat,lon)).to_series()
        attrs={k:str(val) for k,val in ds.attrs.items()}
    alt=pd.DataFrame({'sla_mediana_m':spatial_median,'sla_media_ponderada_m':spatial_mean,'celdas_validas':coverage})
    alt.index=pd.to_datetime(alt.index).to_period('M').to_timestamp()
    if alt.index.duplicated().any(): raise SystemExit('Meses duplicados en altimetría.')
    panel=pd.read_csv(a.panel,parse_dates=['date']); panel=panel[(panel.region=='peru_humboldt')&(panel.depth_band=='surface_2d')]
    if panel.date.duplicated().any(): raise SystemExit('Meses duplicados en GLORYS.')
    gl=panel.set_index('date').zos.rename('glorys_zos_m')
    merged=alt.join(gl,how='outer').sort_index()
    common=merged.loc['1998':'2025',['sla_mediana_m','glorys_zos_m']].dropna()
    if len(common)<96: raise SystemExit(f'Solo {len(common)} meses comunes; insuficiente para comparar.')
    rows=[]
    for name,col in [('Altimetría SLA','sla_mediana_m'),('GLORYS zos','glorys_zos_m')]:
        # Ventana y meses idénticos para ambos productos.
        y=annual(common[col])
        for start in (1998,2003,2010):
            for omit in (False,True):
                subset=y.loc[start:2025]
                if omit: subset=subset[~subset.index.isin(EXTREMES)]
                r=trend(subset)
                if r: rows.append({'serie':name,'inicio':start,'fin':2025,'sin_nino_extremo':omit,**r})
    df=pd.DataFrame(rows)
    if len(df)!=12: raise SystemExit('No hay suficientes años para todos los contrastes; no se emite conclusión.')
    df['q_fdr_12']=multipletests(df.p,method='fdr_bh')[1]
    # Una anomalía común facilita la comparación, sin borrar la tendencia.
    anom=common-common.mean()
    correlation=float(anom.iloc[:,0].corr(anom.iloc[:,1]))
    t0=df[(df.inicio==1998)&(~df.sin_nino_extremo)].set_index('serie')
    x=t0.loc['Altimetría SLA']; y=t0.loc['GLORYS zos']
    delta=float(x.sen_cm_decada-y.sen_cm_decada)
    # Regla descriptiva predefinida, no una prueba de igualdad de pendientes.
    overlap=max(x.ic_inf_cm_decada,y.ic_inf_cm_decada)<=min(x.ic_sup_cm_decada,y.ic_sup_cm_decada)
    equal_sign=np.sign(x.sen_cm_decada)==np.sign(y.sen_cm_decada)
    conclusion='coinciden parcialmente' if equal_sign and overlap else 'no coinciden'
    a.output.mkdir(parents=True,exist_ok=True); a.report.parent.mkdir(parents=True,exist_ok=True)
    merged.rename_axis('date').to_csv(a.output/'serie_mensual.csv'); df.to_csv(a.output/'tendencias.csv',index=False)
    fig,ax=plt.subplots(figsize=(11,4)); ax.plot(anom.index,anom.sla_mediana_m*100,label='Altimetría: mediana espacial'); ax.plot(anom.index,anom.glorys_zos_m*100,label='GLORYS: mediana espacial',alpha=.8)
    ax.set(ylabel='Anomalía respecto a la media común (cm)',title='Nivel del mar frente al Perú: comparación mensual');ax.legend();ax.grid(alpha=.25);fig.tight_layout();fig.savefig(a.output/'comparacion.png',dpi=160);plt.close(fig)
    manifest=a.input.parent/'manifest.json'; provenance=json.loads(manifest.read_text()) if manifest.exists() else {}
    if provenance:
        (a.output/'proveniencia.json').write_text(json.dumps(provenance, indent=2, ensure_ascii=False)+'\n',encoding='utf-8')
    lines=['# Altimetría frente al Perú y GLORYS','','## Conclusión',f'**{conclusion.capitalize()}**, según la regla descriptiva de signo y solapamiento de intervalos individuales. No es una prueba formal de igualdad; no se define una conclusión fuerte de coincidencia sin evaluar incertidumbre conjunta y dependencia.', '',f'Correlación mensual (1998–2025): r = {correlation:.3f}; meses comunes: {len(common)}.',f'Diferencia de pendientes (altimetría − GLORYS): {delta:+.3f} cm/década.','','## Tendencias','','| Serie | Inicio | Sin 1998, 2016, 2023 | n | Sen cm/década | IC 95 % | p | q FDR (12) |','|---|---:|---|---:|---:|---|---:|---:|']
    for _,r in df.iterrows(): lines.append(f'| {r.serie} | {r.inicio} | {"sí" if r.sin_nino_extremo else "no"} | {r.n} | {r.sen_cm_decada:.3f} | [{r.ic_inf_cm_decada:.3f}, {r.ic_sup_cm_decada:.3f}] | {r.p:.5g} | {r.q_fdr_12:.5g} |')
    lines += ['', '## Método y límites','', 'Caja −85 a −70° longitud y −18,35 a −3,38° latitud. Mediana espacial mensual en ambas fuentes; el CSV incluye además media altimétrica ponderada por área y cobertura. Solo meses comunes en 1998–2025. Se resta climatología mensual, se exige 9 meses por año, se aplica Kendall, Sen e intervalo por rangos de Gilbert como en la ronda original. FDR BH sobre las 12 pruebas de esta comparación; no es la familia histórica de 162 y sus q no son comparables directamente.', 'Las pruebas anuales no corrigen autocorrelación; los intervalos son individuales. Las series interpoladas L4 no son mediciones puntuales. GLORYS asimila datos altimétricos, por lo que la comparación no constituye validación plenamente independiente. SLA y zos tienen referencias diferentes; se centran para la correlación y figura.','Las correcciones de marea y ajuste isostático deben verificarse en los metadatos del archivo y el manual. El manual describe tpa_correction, una corrección posterior de deriva instrumental TOPEX-A, y señala que puede aplicarse regionalmente como aproximación; aquí no se ha aplicado. No se ha confirmado el tratamiento de GIA ni de las mareas para esta versión. Los atributos time_coverage originales pueden corresponder a un archivo fuente; la cobertura efectiva debe verificarse en las coordenadas temporales.', '',f'Dataset: {provenance.get("dataset_id", "no verificado: manifiesto ausente")}; versión: {provenance.get("version", "sin verificar")}; descarga UTC: {provenance.get("downloaded_utc", "sin verificar")}.',f'Metadatos globales: `{json.dumps(attrs,ensure_ascii=False)}`', '', 'Fuentes: https://data.marine.copernicus.eu/product/SEALEVEL_GLO_PHY_CLIMATE_L4_MY_008_057/description ; https://documentation.marine.copernicus.eu/PUM/CMEMS-SL-PUM-008-057.pdf ; https://documentation.marine.copernicus.eu/QUID/CMEMS-GLO-QUID-001-030.pdf', '', f'Salidas: `{a.output}`.']
    a.report.write_text('\n'.join(lines)+'\n',encoding='utf-8');print('\n'.join(lines[:8]));print(df.to_string(index=False))

if __name__=='__main__': main()
