"""Preregistered tests; local data only. Run without -I."""
import argparse, hashlib, json, platform
from pathlib import Path
import numpy as np
import pandas as pd
import scipy
from scipy import stats, linalg
from bloque1_teleconexion import cargar, pn, REPO, R_DATA
from utils_pruebas import anomalia_mensual, parcial_multi, corr_neff, fdr, EXTREMOS
SEED=20261115
B=2000
LAGS=(0,12,24,36,48,60)
REGIONS=('bellingshausen','peninsula_antarctica','south_pacific_intermediate','south_pacific_subtropical')
VARS=('no3','po4','o2','thetao','so')
TARGETS=(('no3','surface_0_5m'),('no3','subsurface_100_200m'),('po4','subsurface_100_200m'),('o2','subsurface_100_200m'),('chl','surface_0_5m'))
OUT=REPO/'data/tablas_pruebas_pendientes'
DOC=Path(__file__).parent
PREFIX='bloque5_nutrientes_'
def align(x,y,z,k):
    return pd.Series(x).shift(k).to_numpy(),y,np.column_stack([z,pd.Series(z).shift(k).to_numpy()])
def partial(x,y,Z,mask=None):
    return parcial_multi(x if mask is None else np.where(mask,x,np.nan),y if mask is None else np.where(mask,y,np.nan),Z)
def fields(r,prefix):
    return {prefix+k:np.nan if r is None else r[i] for i,k in enumerate(('r','n','neff','p'))}
def checks(x,y,z,k,idx):
    xx,yy,Z=align(x,y,z,k);prev=idx-pd.DateOffset(months=k)
    masks=((idx.year<=2011)&(prev.year>=1998)&(prev.year<=2011),(idx.year>=2012)&(prev.year>=2012),~idx.year.isin(EXTREMOS)&~prev.year.isin(EXTREMOS))
    full=partial(xx,yy,Z);a,b,c=[partial(xx,yy,Z,m) for m in masks]
    return {**fields(a,'half1_'),**fields(b,'half2_'),**fields(c,'noext_'),'same_sign_halves':full is not None and a is not None and b is not None and np.sign(a[0])==np.sign(b[0])==np.sign(full[0])}
def surrogate(x,y,z,k,observed,rng):
    shifts=rng.integers(24,len(x)-24+1,size=B);draws=[]
    for shift in shifts:
        r=partial(*align(np.roll(x,int(shift)),y,z,k))
        draws.append((int(shift),np.nan if r is None else r[0]))
    return (1+sum(not np.isfinite(r) or abs(r)>=abs(observed) for _,r in draws))/(B+1),draws

def selftest():
    rng=np.random.default_rng(SEED);n=336;x=rng.normal(size=n);z=rng.normal(size=n)
    y=rng.normal(scale=.15,size=n);y[24:]+=x[:-24]
    r=partial(*align(x,y,z,24));q=fdr(np.array([r[3]]+[1.]*1199))[0];emp,_=surrogate(x,y,z,24,r[0],rng)
    assert q<.05 and emp<.05,(q,emp)
    print(f'SELFTEST lag24: r={r[0]:.6f}; q={q:.6g}; empirical={emp:.6g} PASS')
    # Diagnostic: deterministic waves are not independent stochastic noise.
    t=np.arange(n);sx=np.sin(2*np.pi*t/240);sy=np.sin(2*np.pi*t/260+.4)
    r=partial(*align(sx,sy,z,0));wave_p,_=surrogate(sx,sy,z,0,r[0],rng)
    print(f'DIAGNOSTIC deterministic waves: empirical={wave_p:.6g}; false positive limitation retained')
    null_rng=np.random.default_rng(SEED+2)
    innovation=null_rng.normal(size=(2,1336));noise=np.zeros_like(innovation)
    for i in range(1,1336):noise[:,i]=.98*noise[:,i-1]+innovation[:,i]
    x,y=noise[:,-336:];r=partial(*align(x,y,z,0));emp,_=surrogate(x,y,z,0,r[0],rng)
    assert emp>=.05,emp
    print(f'SELFTEST independent AR(1) .98 noise: r={r[0]:.6f}; empirical={emp:.6g} PASS')

def run():
    mon,pan,idx=cargar()
    if pan.duplicated(['date','region','depth_band']).any():raise ValueError('Duplicate region/depth/date')
    missing=[];P={};T={}
    def get(reg,band,col):
        if col not in pan:
            missing.append(f'{reg}/{band}/{col}: missing column');return pd.Series(np.nan,index=idx).to_numpy()
        a=pn(pan,idx,reg,band,col)
        if a.notna().sum()<36:missing.append(f'{reg}/{band}/{col}: {a.notna().sum()} available months')
        return anomalia_mensual(a).to_numpy()
    for reg in REGIONS:
        for var in VARS:P[f'{reg}|intermediate_200_500m|{var}']=get(reg,'intermediate_200_500m',var+'_anom')
    for reg in ('peru_humboldt','transition_humboldt'):
        for var,band in TARGETS:T[f'{reg}|{band}|{var}']=get(reg,band,var+'_anom')
    for col in ('nino12_psl_c','oni_c'):
        if col not in mon:missing.append(col+': missing control');mon[col]=np.nan
    z=anomalia_mensual(mon.nino12_psl_c).to_numpy();oni=anomalia_mensual(mon.oni_c).to_numpy()
    rows=[]
    for p,x in P.items():
        for target,y in T.items():
            for k in LAGS:
                xx,yy,Z=align(x,y,z,k);m=np.isfinite(xx)&np.isfinite(yy)&np.isfinite(Z).all(axis=1)
                raw=corr_neff(xx[m],yy[m]);par=partial(xx,yy,Z)
                rows.append({'test_id':len(rows),'predictor':p,'target':target,'lag_months':k,'complete_pairs':int(m.sum()),**fields(raw,'raw_'),**fields(par,'partial_'),**checks(x,y,z,k,idx)})
    df=pd.DataFrame(rows);assert len(df)==1200
    for kind in ('raw','partial'):df[kind+'_q']=fdr(df[kind+'_p'].fillna(1).to_numpy())
    candidates=sorted(set(df[df.partial_p.notna()].sort_values(['partial_p','test_id']).head(20).test_id)|set(df[df.partial_q<.05].test_id))
    rng=np.random.default_rng(SEED);surr=[];cal=[]
    for i,test_id in enumerate(candidates):
        row=df.loc[test_id];emp,draws=surrogate(P[row.predictor],T[row.target],z,int(row.lag_months),row.partial_r,rng)
        surr.extend({'test_id':test_id,'draw':j,'shift_months':s,'r_surrogate':r} for j,(s,r) in enumerate(draws))
        cal.append({'test_id':test_id,'p_empirical':emp,'B':B,'invalid_surrogates':sum(not np.isfinite(r) for _,r in draws),'unique_shifts':len(set(s for s,_ in draws))})
        print(f'Surrogates {i+1}/{len(candidates)} test={test_id} empirical={emp:.6f}',flush=True)
    calibration=pd.DataFrame(cal,columns=['test_id','p_empirical','B','invalid_surrogates','unique_shifts'])
    df=df.merge(calibration,on='test_id',how='left',validate='one_to_one')
    df['passes_q']=df.partial_q<.05;df['passes_surrogates']=df.p_empirical<.05;df['passes_extremes']=df.noext_p<.05
    df['passes_before_sign']=df.passes_q&df.passes_surrogates&df.same_sign_halves&df.passes_extremes
    df['finding']=df.passes_before_sign&(df.partial_r>0);df['unexpected_sign']=df.passes_before_sign&(df.partial_r<0)
    onis=[]
    for _,row in df[df.passes_before_sign].iterrows():
        k=int(row.lag_months);x=P[row.predictor];y=T[row.target];r=partial(*align(x,y,oni,k))
        onis.append({'test_id':row.test_id,**fields(r,'oni_'),**checks(x,y,oni,k,idx),'corroborated':r is not None and r[3]<.05 and np.sign(r[0])==np.sign(row.partial_r)})
    chosen=int(np.random.default_rng(SEED+1).choice(df[df.partial_r.notna()].test_id))
    row=df.loc[df.test_id==chosen].iloc[0];xx,yy,Z=align(P[row.predictor],T[row.target],z,int(row.lag_months))
    m=np.isfinite(xx)&np.isfinite(yy)&np.isfinite(Z).all(axis=1);A=np.column_stack([np.ones(m.sum()),Z[m]])
    rx=xx[m]-A@linalg.lstsq(A,xx[m])[0];ry=yy[m]-A@linalg.lstsq(A,yy[m])[0]
    r=float(stats.pearsonr(rx,ry).statistic);ac=float(stats.pearsonr(rx[:-1],rx[1:]).statistic*stats.pearsonr(ry[:-1],ry[1:]).statistic)
    ne=max(3.,len(rx)*(1-ac)/(1+ac)) if ac<1 else 3.
    p=float(2*stats.t.sf(abs(r)*np.sqrt((ne-2)/max(1e-9,1-r*r)),ne-2))
    assert abs(r-row.partial_r)<1e-10 and abs(p-row.partial_p)<1e-10
    verify=pd.DataFrame([{'test_id':chosen,'r_scipy':r,'r_utility':row.partial_r,'p_scipy_effective':p,'p_utility':row.partial_p,'n_eff_scipy':ne}])
    power=[];critical=stats.norm.isf(.05/1200/2)
    for effect in (.2,.3,.5):
        for k in LAGS:
            ne=df.loc[df.lag_months==k,'partial_neff'].dropna().to_numpy();mu=np.arctanh(effect)*np.sqrt(np.maximum(0,ne-3-2))
            pow=stats.norm.sf(critical-mu)+stats.norm.cdf(-critical-mu)
            power.append({'true_r':effect,'lag_months':k,'median_neff':np.median(ne),'median_power':np.median(pow),'min_power':np.min(pow),'max_power':np.max(pow)})
    outputs={'todas':df,'supervivientes':df[df.finding|df.unexpected_sign],'sustitutos':pd.DataFrame(surr,columns=['test_id','draw','shift_months','r_surrogate']),'calibracion':calibration,'oni':pd.DataFrame(onis,columns=None if onis else ['test_id','oni_r','oni_n','oni_neff','oni_p','corroborated']),'verificacion':verify,'potencia_exploratoria':pd.DataFrame(power)}
    for name,table in outputs.items():table.to_csv(OUT/(PREFIX+name+'.csv'),index=False,float_format='%.17g',encoding='utf-8',lineterminator='\n')
    paths=[Path(R_DATA)/'drive_aaron/connectivity_panel_monthly.csv',Path(R_DATA)/'pruebas/json_pagina/monitor_data.json']
    meta={'seed':SEED,'B':B,'missing':missing,'hashes':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},'versions':{'python':platform.python_version(),'numpy':np.__version__,'pandas':pd.__version__,'scipy':scipy.__version__},'nino_available':int(np.isfinite(z).sum()),'oni_available':int(np.isfinite(oni).sum())}
    (OUT/(PREFIX+'metadatos.json')).write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    report()

def counts(d,cal):
    return {'Familia primaria':len(d),'Calculables':int(d.partial_p.notna().sum()),'p cruda < .05':int((d.raw_p<.05).sum()),'q cruda < .05':int((d.raw_q<.05).sum()),'p parcial < .05':int((d.partial_p<.05).sum()),'q parcial < .05':int(d.passes_q.sum()),'Mismo signo en mitades (toda la familia)':int(d.same_sign_halves.sum()),'p sin extremos < .05 (toda la familia)':int(d.passes_extremes.sum()),'Sustitutos evaluados':len(cal),'Sustitutos p < .05 (selección calibrada)':int((cal.p_empirical<.05).sum()),'q + sustitutos':int((d.passes_q&d.passes_surrogates).sum()),'+ signo consistente en mitades':int((d.passes_q&d.passes_surrogates&d.same_sign_halves).sum()),'+ p sin extremos < .05':int(d.passes_before_sign.sum()),'+ signo positivo (hallazgos)':int(d.finding.sum()),'Signo inesperado':int(d.unexpected_sign.sum())}
def md(t):
    return '| '+' | '.join(map(str,t.columns))+' |\n| '+' | '.join(['---']*len(t.columns))+' |\n'+'\n'.join('| '+' | '.join(str(x).replace('|',r'\|') for x in r)+' |' for r in t.itertuples(index=False,name=None))
def report():
    d=pd.read_csv(OUT/(PREFIX+'todas.csv'));cal=pd.read_csv(OUT/(PREFIX+'calibracion.csv'));power=pd.read_csv(OUT/(PREFIX+'potencia_exploratoria.csv'));meta=json.loads((OUT/(PREFIX+'metadatos.json')).read_text(encoding='utf-8'))
    c=counts(d,cal);top=d.sort_values(['partial_p','test_id']).head(10)[['test_id','predictor','target','lag_months','raw_r','partial_r','partial_neff','partial_p','partial_q','p_empirical','half1_r','half2_r','noext_p']]
    conclusion='no se detecta vínculo con estos datos' if not d.finding.any() else f'{int(d.finding.sum())} asociaciones cumplen el criterio; no demuestran transporte ni causalidad'
    text=f'''# Resultados: nutrientes y masas de agua, largo plazo

Preregistro confirmado en commit 7a64339, con enmienda de selftest db6c14f antes de ejecutar datos reales. Conclusión: **{conclusion}**.

## Método confirmatorio

Reanálisis, no observaciones directas. Veinte predictores en 200–500 m, diez objetivos y seis retrasos; 1998–2025. Se reutilizan cargar/pn de bloque 1 y parcial_multi/corr_neff/fdr de utils, sin modificarlos. Anomalías recentradas por mes; Niño 1+2 en t y t-k; r cruda y parcial sobre los mismos pares completos. FDR sobre las 1200 filas, p=1 para filas no calculables. No se rellenan huecos. Mitades y exclusiones afectan ambos instantes; se exige el signo completo en ambas mitades. ONI se aplica a los que pasan antes del filtro positivo, sin añadir un criterio nuevo.

Sustitutos: 2000 desplazamientos por fila, offsets en [24,312], con reemplazo (289 offsets posibles). Se rota X antes del lag, no Y ni los controles. Estadístico bilateral |r parcial|; p=(1+excedencias)/(2001). Un sustituto inválido cuenta conservadoramente como excedencia. Selección: top 20 p parciales y todos con q<.05. No es un test máximo sobre retrasos. Tamaño efectivo AC1 de residuos y p con neff-2, exactamente como utils, sin descuento explícito de controles.

## Conteos desde las tablas

{md(pd.DataFrame(list(c.items()),columns=['Filtro','Número']))}

## Pares más altos, aunque no sean hallazgos

{md(top.round(8))}

Mediana |r| cruda {d.raw_r.abs().median():.6f}; parcial {d.partial_r.abs().median():.6f}. De {int((d.raw_q<.05).sum())} filas con q cruda <.05, {int(((d.raw_q<.05)&(d.partial_q>=.05)).sum())} dejan de pasar tras el control Niño 1+2.

Hallazgos a lag 0: {int((d.finding&(d.lag_months==0)).sum())}; a 12–60 meses: {int((d.finding&(d.lag_months>0)).sum())}. Un vínculo contemporáneo no demuestra transporte lento. Negativos que pasan los otros filtros: {int(d.unexpected_sign.sum())}; "signo inesperado, no respalda la hipótesis". CSV supervivientes/oni sin filas significa cero casos elegibles.

## Potencia estimada (exploratoria)

{md(power.round(6))}

Aproximación Fisher-z con neff, dos controles y Bonferroni .05/1200. No es potencia exacta del criterio compuesto; la potencia conjunta puede ser menor. No estima la probabilidad de que la hipótesis sea verdadera. neff mediano {d.partial_neff.median():.3f}, mínimo {d.partial_neff.min():.3f}. Con 28 años y lags de años quedan pocos grados de libertad efectivos. Un nulo no prueba que no exista vínculo lento; el registro no lo detecta con este diseño.

## Datos faltantes y limitaciones

{chr(10).join('- '+x for x in meta['missing']) if meta['missing'] else '- Ninguna combinación solicitada falta por completo; complete_pairs de cada fila registra la disponibilidad real.'}

Niño 1+2 disponible {meta['nino_available']} meses; ONI {meta['oni_available']}. Los lags recortan la muestra y se excluyen cruces entre mitades. No se incluyeron afloramiento calculado, trazadores, perfiles Argo/BGC-Argo ni biomasa acústica; se necesitan esas mediciones y registros más largos e independientes para probar rutas y efectos biológicos. thetao/so no identifican por sí solos masas ni trayectorias.

AC1 no representa toda la memoria de baja frecuencia. Hay dependencia entre regiones/productos del mismo modelo. Los desplazamientos circulares introducen una unión artificial del registro y no representan 2000 historias independientes. Pocos grados efectivos, no estacionariedad y huecos limitan la interpretación. Ni un positivo demostraría transporte o causalidad. No se probaron otros lags/regiones; solo potencia se declara exploratoria.

## Selftest y error observado

El primer selftest pasó la señal sintética a 24 meses (r=0.986749, q=1.02301e-243, p empírico=0.00049975), pero su aserción sobre dos ondas deterministas falló (AssertionError: 0.0004997501249375312). No se ocultó ni se cambió el criterio de sustitutos. Se registró la enmienda db6c14f antes de datos reales para usar el nulo pedido de ruido autocorrelacionado: dos AR(1) independientes, coeficiente .98, semilla 20261117 y 1000 pasos de calentamiento. Ese selftest pasó (r=-0.091326, p empírico=0.548226). La señal y el ruido se verificaron con 2000 sustitutos cada uno. Para la señal, la corrección q usa una familia sintética de 1200 con las restantes p=1; no es una simulación de potencia de toda la búsqueda.

El falso positivo de las ondas se conserva como diagnóstico exploratorio: la restricción de offsets puede dar una calibración inadecuada con formas no estacionarias. Un único ejemplo de ruido que pasa no valida en general el nivel de falsos positivos. Esto refuerza la cautela, incluso para los pares reales con p empírico pequeño.

## Verificación

Se ejecutó dos veces con la misma semilla: los siete CSV y metadatos JSON resultaron idénticos byte por byte (SHA256). Los hashes de entradas se registraron sin modificar originales. Una comprobación inicial del script verificador emitió Pandas4Warning por float_precision; se sustituyó ese argumento por conversores float explícitos y se repitió la verificación.

Una fila calculable al azar, semilla 20261116, se verifica con scipy.linalg.lstsq y scipy.stats.pearsonr; p efectivo con t de SciPy. Coincide a tolerancia 1e-10 (ver verificacion.csv). No se confunde el p de Pearson independiente con el p efectivo. El informe se genera desde CSV y --verify-report revisa conteos y criterios.

Ejecutar con PYTHONIOENCODING=utf-8 y sin -I: python docs/pruebas_pendientes/bloque5_nutrientes_largo_plazo.py --selftest; luego sin opciones. --report-only regenera el informe, --verify-report comprueba las cifras. Semilla {SEED}. Versiones: {meta['versions']}. Hashes SHA256 de entradas en metadatos.json.
'''
    (DOC/'RESULTADOS_NUTRIENTES_LARGO_PLAZO.md').write_text(text,encoding='utf-8');print(json.dumps(c,ensure_ascii=False,indent=2))
def verify_report():
    d=pd.read_csv(OUT/(PREFIX+'todas.csv'));cal=pd.read_csv(OUT/(PREFIX+'calibracion.csv'));s=(DOC/'RESULTADOS_NUTRIENTES_LARGO_PLAZO.md').read_text(encoding='utf-8')
    assert len(d)==1200
    for label,n in counts(d,cal).items():assert f'| {label} | {n} |' in s,(label,n)
    assert not (d.finding&~(d.passes_q&d.passes_surrogates&d.same_sign_halves&d.passes_extremes&(d.partial_r>0))).any()
    surrogate_rows=pd.read_csv(OUT/(PREFIX+'sustitutos.csv'),converters={'r_surrogate':lambda v:float(v) if v else np.nan})
    original=pd.read_csv(OUT/(PREFIX+'todas.csv'),converters={'partial_r':lambda v:float(v) if v else np.nan}).set_index('test_id')
    for _,row in cal.iterrows():
        group=surrogate_rows[surrogate_rows.test_id==row.test_id]
        assert len(group)==B and group.shift_months.between(24,312).all()
        r=original.loc[int(row.test_id),'partial_r']
        empirical=(1+((group.r_surrogate.abs()>=abs(r))|group.r_surrogate.isna()).sum())/(B+1)
        assert abs(empirical-row.p_empirical)<1e-14
    survivors=pd.read_csv(OUT/(PREFIX+'supervivientes.csv'))
    assert set(survivors.test_id)==set(d.loc[d.finding|d.unexpected_sign,'test_id'])
    print('Report counts, surrogate p-values, survivors and finding criteria: PASS')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--selftest',action='store_true');p.add_argument('--report-only',action='store_true');p.add_argument('--verify-report',action='store_true');a=p.parse_args()
    if a.selftest:selftest()
    elif a.report_only:report()
    elif a.verify_report:verify_report()
    else:run()
