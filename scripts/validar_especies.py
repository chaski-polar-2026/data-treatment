#!/usr/bin/env python3
"""Validate sourced species tables."""
import csv, re, sys
from pathlib import Path
DATA=Path(__file__).resolve().parents[1]/"data"/"especies"
def load(n):
    with (DATA/n).open(encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
TEMPERATURE_BASES = {"field_seasonal_observation", "field_depth_mixed_observation", "bottom_temperature_cruise", "laboratory_treatment"}
DEPTH_BASES = {"distribution_range", "dive_depth_observation", "survey_stratum"}
SCHEMA_FIELDS = {"temperature_basis", "temperature_comparable", "depth_basis"}

def validate_schema(r):
    errors = []
    sid = r.get("id", "unknown")
    basis = r.get("temperature_basis", "")
    comparable = r.get("temperature_comparable", "")
    has_temperature = bool(r.get("temperature_min_c") or r.get("temperature_max_c"))
    if has_temperature and not basis:
        errors.append(f"{sid}: temperature_basis required for recorded temperature")
    if basis and basis not in TEMPERATURE_BASES:
        errors.append(f"{sid}: invalid temperature_basis: {basis}")
    if has_temperature and comparable not in {"true", "false"}:
        errors.append(f"{sid}: temperature_comparable must be true or false")
    if comparable == "true" and basis not in {"field_seasonal_observation", "bottom_temperature_cruise"}:
        errors.append(f"{sid}: temperature_comparable cannot be true for {basis or 'missing basis'}")
    if not has_temperature and (basis or comparable):
        errors.append(f"{sid}: temperature metadata requires recorded temperature")
    depth = r.get("depth_basis", "")
    if (r.get("depth_min_m") or r.get("depth_max_m")) and not depth:
        errors.append(f"{sid}: depth_basis required for recorded depth")
    if depth and depth not in DEPTH_BASES:
        errors.append(f"{sid}: invalid depth_basis: {depth}")
    if has_temperature:
        note = r.get("temperature_note", "").casefold()
        recorded = any(word in note for word in ("observations", "field", "treatment temperatures"))
        not_limits = bool(re.search(r"\bnot (?:thermal )?limits\b", note))
        if not recorded or not not_limits:
            errors.append(f"{sid}: temperature_note must describe observations or treatments, not limits")
    return errors

def validate_optimum(r, mapped):
    if not r.get("temperature_optimum_c"):
        return []
    sid = r["id"]
    errors = []
    if not r.get("temperature_optimum_note", "").strip():
        errors.append(f"{sid}: temperature_optimum_note required with study type and scope")
    for field in ("temperature_optimum_c", "temperature_optimum_note"):
        citations = mapped.get((sid, field), [])
        if not any(c.get("valor") == r.get(field) and c.get("cita_corta", "").strip() for c in citations):
            errors.append(f"{sid}: {field} requires matching sourced evidence")
    return errors

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
        errors.extend(validate_schema(r))
        for field,value in r.items():
            if field == "notes": value = value.split(" Review status:", 1)[0]
            if value and field not in structural | SCHEMA_FIELDS and not any(a["valor"]==value and a.get("cita_corta","").strip() for a in mapped.get((sid,field),[])):
                errors.append(f"{sid}.{field}: populated value lacks matching sourced quote")
        for lo,hi in (("depth_min_m","depth_max_m"),("temperature_min_c","temperature_max_c")):
            if r.get(lo) and r.get(hi) and float(r[lo])>float(r[hi]):errors.append(f"{sid}: {lo} exceeds {hi}")
        lo,hi,opt=(r.get(k,"") for k in ("temperature_min_c","temperature_max_c","temperature_optimum_c"))
        errors.extend(validate_optimum(r, mapped))
        if any((lo,hi,opt)):
            if not lo or not hi:errors.append(f"{sid}: temperature min and max both required")
            if not r.get("temperature_note","").strip():errors.append(f"{sid}: temperature_note required")
            if not mapped.get((sid,"temperature_min_c")) or not mapped.get((sid,"temperature_max_c")):errors.append(f"{sid}: temperature range needs source")
            # Recorded field endpoints do not constrain a separately sourced experimental optimum.
    if errors:
        print("Species validation failed:");[print('- '+x) for x in errors];return 1
    print(f"Species validation passed ({len(species)} records; {len(refs)} cited field values).")
    return 0
if __name__=="__main__":sys.exit(main())
