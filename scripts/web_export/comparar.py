"""Compare generated web data against an explicitly supplied read-only directory."""
import argparse, hashlib, json, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'docs/pruebas_pendientes'))
from config_datos import WEB_EXPORT

def parse(raw):
    text=raw.decode('utf-8-sig')
    return json.loads(text[text.index('{'):text.rindex('}')+1])
def differences(a,b,path=''):
    if isinstance(a,dict) and isinstance(b,dict):
        result=[]
        for key in sorted(a.keys()|b.keys()):
            result.extend([path+'/'+key] if key not in a or key not in b else differences(a[key],b[key],path+'/'+key))
        return result
    if isinstance(a,list) and isinstance(b,list):
        result=[path+'/length'] if len(a)!=len(b) else []
        for i,(x,y) in enumerate(zip(a,b)):result.extend(differences(x,y,path+'/'+str(i)))
        return result
    return [] if a==b else [path]
def main():
    p=argparse.ArgumentParser();p.add_argument('--public-data',type=Path,required=True);a=p.parse_args();report=[]
    for name in ('tendencias-ronda.json','nino-relaciones.json','monitor-data.js'):
        generated=(WEB_EXPORT/name).read_bytes();published=(a.public_data/name).read_bytes()
        paths=differences(parse(generated),parse(published))
        report.append({'file':name,'identical_bytes':generated==published,'equal_json':not paths,'differing_paths':paths,'generated_sha256':hashlib.sha256(generated).hexdigest(),'published_sha256':hashlib.sha256(published).hexdigest()})
        print(name,report[-1]['identical_bytes'],len(paths),'differing JSON paths')
    (WEB_EXPORT/'comparacion_web.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return 1 if any(not r['identical_bytes'] for r in report) else 0
if __name__=='__main__':raise SystemExit(main())
