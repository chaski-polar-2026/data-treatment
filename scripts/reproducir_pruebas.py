"""Reproduce existing analyses in isolated outputs and compare with Git snapshots."""
import argparse, hashlib, json, os, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/'docs/pruebas_pendientes'
sys.path.insert(0,str(SCRIPTS))
from config_datos import DATA, OUTPUT, TABLES

def main():
    p=argparse.ArgumentParser();p.add_argument('--rapido',action='store_true');p.add_argument('--bloques',default='1,3,4,5,vecinos');a=p.parse_args()
    manifest=json.loads((DATA/'manifest.json').read_text(encoding='utf-8'))
    for item in manifest:
        if item.get('included',True):
            path=DATA/item['path']
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=item['sha256']:
                raise ValueError('Missing or changed input: '+item['path']+'; see data/inputs/LEEME.md')
    print('Input SHA256: PASS',flush=True)
    env=os.environ.copy();env['PYTHONIOENCODING']='utf-8'
    jobs={'1':'bloque1_teleconexion.py','3':'bloque3_perspectiva.py','4':'bloque4_desembarques.py','5':'bloque5_nutrientes_largo_plazo.py','vecinos':'antartida_vecinos.py'}
    results=[]
    for key in a.bloques.split(','):
        script=jobs[key];args=[sys.executable,str(SCRIPTS/script)]
        if key=='5' and a.rapido:args.append('--rapido')
        print('RUN',script,flush=True)
        run=subprocess.run(args,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8')
        (OUTPUT/(script+'.log')).write_text(run.stdout,encoding='utf-8')
        print(run.stdout[-2000:],flush=True)
        results.append({'script':script,'returncode':run.returncode})
    comparisons=[]
    for generated in sorted((OUTPUT/'data').rglob('*')):
        if not generated.is_file() or generated.suffix not in ('.csv','.json'):continue
        relative=generated.relative_to(OUTPUT).as_posix()
        reference=subprocess.run(['git','show','HEAD:'+relative],cwd=ROOT,capture_output=True)
        if reference.returncode:
            reference_path=ROOT/relative
            # A clean archive has no .git: committed files serve as the baseline.
            baseline=reference_path.read_bytes() if reference_path.exists() else None
        else:baseline=reference.stdout
        equal=baseline==generated.read_bytes() if baseline is not None else False
        text_equal=baseline is not None and baseline.replace(b'\r\n',b'\n')==generated.read_bytes().replace(b'\r\n',b'\n')
        smoke=a.rapido and generated.name.startswith('bloque5_nutrientes_')
        state='IDENTICAL' if equal else 'LINE_ENDINGS_ONLY' if text_equal else 'RAPIDO_NOT_EQUIVALENT' if smoke else 'DIFFERENT' if baseline is not None else 'NO_BASELINE'
        if baseline is not None and generated.name=='bloque5_nutrientes_metadatos.json' and not equal:
            old=json.loads(baseline);new=json.loads(generated.read_bytes())
            same_inputs=sorted(old.get('hashes',{}).values())==sorted(new.get('hashes',{}).values())
            if same_inputs and {k:v for k,v in old.items() if k!='hashes'}=={k:v for k,v in new.items() if k!='hashes'}:state='METADATA_PATHS_ONLY'
        comparisons.append({'file':relative,'status':state});print(state,relative,flush=True)
    report={'quick':a.rapido,'python':sys.version,'jobs':results,'comparisons':comparisons}
    (OUTPUT/'comparacion.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return 1 if any(r['returncode'] for r in results) or any(c['status']=='DIFFERENT' for c in comparisons) else 0
if __name__=='__main__':raise SystemExit(main())
