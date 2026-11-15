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


def main() -> None:
    species = rows(DATA / "especies.csv")
    references = rows(DATA / "especies_fuentes.csv")
    by_species: dict[str, dict[str, list[dict[str, str]]]] = {}
    for ref in references:
        by_species.setdefault(ref["id_especie"], {}).setdefault(ref["campo"], []).append(
            {"source_id": ref["id_fuente"], "page_or_table": ref["pagina_o_tabla"]}
        )

    result = []
    for item in species:
        sourced: dict[str, object] = {}
        for field, value in item.items():
            if not value:
                continue
            if field in {"id", "common_name_en", "common_name_es", "group", "evidence_level", "flags"}:
                sourced[field] = value
            elif by_species.get(item["id"], {}).get(field):
                sourced[field] = value
            else:
                continue
        sourced["sources"] = by_species.get(item["id"], {})
        result.append(sourced)

    output = DATA / "especies.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
