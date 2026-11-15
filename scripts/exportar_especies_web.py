#!/usr/bin/env python3
"""Export sourced species fields as JSON for later web integration."""

from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "especies"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def export_species(species, references):
    by_species = {}
    for ref in references:
        by_species.setdefault(ref["id_especie"], {}).setdefault(ref["campo"], []).append({
            "source_id": ref["id_fuente"], "page_or_table": ref["pagina_o_tabla"], "short_quote": ref["cita_corta"]})
    result = []
    caveats = {
        "laboratory_treatment": "Laboratory treatment temperatures, not a field range",
        "field_depth_mixed_observation": "Temperatures recorded at different depths, not a single field range",
    }
    for item in species:
        refs = by_species.get(item["id"], {})
        sourced = {}
        for field, value in item.items():
            if any(word in field.casefold() for word in ("preferred", "optimum", "suitability")):
                continue
            if value and (field in {"id", "common_name_en", "common_name_es", "group", "evidence_level", "flags"} or field in refs):
                if field not in {"temperature_min_c", "temperature_max_c", "depth_min_m", "depth_max_m"}:
                    sourced[field] = value
        number = lambda key: float(item[key]) if item.get(key) else None
        basis = item.get("temperature_basis", "")
        comparable = item.get("temperature_comparable") == "true"
        temperature = {
            "min": number("temperature_min_c"), "max": number("temperature_max_c"),
            "basis": basis or None, "comparable": comparable, "use_in_comparison": comparable,
            "label": "Temperatures recorded in Peru (observations, not limits)",
            "source": {k: refs.get(k, []) for k in ("temperature_min_c", "temperature_max_c", "temperature_note")},
        }
        if not comparable:
            temperature["caveat"] = caveats.get(basis, "No sourced temperature range recorded")
        else:
            temperature["caveat"] = "Recorded observations, not tolerance limits. Compare only matching measurement depths and contexts."
        sourced["recorded_temperature"] = temperature
        depth_basis = item.get("depth_basis", "")
        sourced["recorded_depth"] = {
            "min": number("depth_min_m"), "max": number("depth_max_m"), "depth_basis": depth_basis or None,
            "label": "Deepest recorded dive" if depth_basis == "dive_depth_observation" else "Recorded depth (not a species limit)",
            "source": {k: refs.get(k, []) for k in ("depth_min_m", "depth_max_m")},
        }
        sourced["sources"] = {k:v for k,v in refs.items() if not any(word in k.casefold() for word in ("preferred", "optimum", "suitability"))}
        result.append(sourced)
    return result


def main() -> None:
    result = export_species(rows(DATA / "especies.csv"), rows(DATA / "especies_fuentes.csv"))
    output = DATA / "especies.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
