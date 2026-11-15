#!/usr/bin/env python3
"""Validate sourced species tables."""
import csv, re, sys
from pathlib import Path
DATA=Path(__file__).resolve().parents[1]/"data"/"especies"
def load(n):
    with (DATA/n).open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def main():
    errors=[]; species=load("especies.csv"); refs=load("especies_fuentes.csv"); sources=load("fuentes.csv")
    source={x["id_fuente"]:x for x in sources}; ids={x["id"] for x in species}; mapped={}
    if not refs or "cita_corta" not in refs[0]:errors.append("especies_fuentes.csv requires cita_corta")
    for x in refs:
        key=(x["id_especie"],x["campo"]);mapped.setdefault(key,[]).append(x)
        if key[0] not in ids:errors.append(f"unknown species {key[0]}")
        if x["id_fuente"] not in source:errors.append(f"unknown source {x['id_fuente']}")
        q=x.get("cita_corta","").strip()
        if not q:errors.append(f"{key}: empty cita_corta")
        if len(q.split())>15:errors.append(f"{key}: cita_corta exceeds 15 words")
        if x["pagina_o_tabla"].casefold()=="abstract":
            abstract=source.get(x["id_fuente"],{}).get("abstract_text","")
            norm=lambda s:re.sub(r"\W+"," ",s.casefold()).strip()
            if not abstract or norm(q) not in norm(abstract):errors.append(f"{key}: quote absent from source abstract")
    structural={"id","common_name_en","common_name_es","scientific_name_accepted","aphia_id","group","evidence_level","flags"}
    for r in species:
        sid=r["id"]
        for field,value in r.items():
            if value and field not in structural and not any(a["valor"]==value and a.get("cita_corta","").strip() for a in mapped.get((sid,field),[])):
                errors.append(f"{sid}.{field}: populated value lacks matching sourced quote")
        for lo,hi in (("depth_min_m","depth_max_m"),("temperature_min_c","temperature_max_c")):
            if r.get(lo) and r.get(hi) and float(r[lo])>float(r[hi]):errors.append(f"{sid}: {lo} exceeds {hi}")
        lo,hi,opt=(r.get(k,"") for k in ("temperature_min_c","temperature_max_c","temperature_optimum_c"))
        if any((lo,hi,opt)):
            if not lo or not hi:errors.append(f"{sid}: temperature min and max both required")
            if not r.get("temperature_note","").strip():errors.append(f"{sid}: temperature_note required")
            if not mapped.get((sid,"temperature_min_c")) or not mapped.get((sid,"temperature_max_c")):errors.append(f"{sid}: temperature range needs source")
            if opt and lo and hi and not float(lo)<=float(opt)<=float(hi):errors.append(f"{sid}: optimum outside min/max")
    if errors:
        print("Species validation failed:");[print('- '+x) for x in errors];return 1
    print(f"Species validation passed ({len(species)} records; {len(refs)} cited field values).")
    return 0
if __name__=="__main__":sys.exit(main())
