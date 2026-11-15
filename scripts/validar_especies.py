#!/usr/bin/env python3
"""Validate the sourced species-data tables."""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "especies"
SPECIES_FILE = DATA / "especies.csv"
VALUE_SOURCES_FILE = DATA / "especies_fuentes.csv"
SOURCES_FILE = DATA / "fuentes.csv"
STRUCTURAL_FIELDS = {
    "id", "common_name_en", "common_name_es", "scientific_name_accepted",
    "aphia_id", "group", "evidence_level", "flags",
}
TEXT_FIELDS = {
    "common_name_en", "habitat_summary", "temperature_note", "season_note",
    "el_nino_response_note", "peru_coast_range_note", "fishery_note", "notes",
}
SPANISH_MARKERS = re.compile(
    r"\b(?:que|para|con|una|uno|los|las|por|del|desde|hasta|según|especie|"
    r"pesquería|profundidad|costa|pendiente|fuente|datos)\b",
    re.IGNORECASE,
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    errors: list[str] = []
    species = read_csv(SPECIES_FILE)
    field_sources = read_csv(VALUE_SOURCES_FILE)
    sources = read_csv(SOURCES_FILE)

    source_ids = {row["id_fuente"] for row in sources}
    species_ids = {row["id"] for row in species}
    source_map: dict[tuple[str, str], list[str]] = {}
    for row in field_sources:
        key = (row["id_especie"], row["campo"])
        source_map.setdefault(key, []).append(row["valor"])
        if row["id_especie"] not in species_ids:
            errors.append(f"Unknown species id in source map: {row['id_especie']}")
        if row["id_fuente"] not in source_ids:
            errors.append(f"Unknown source id: {row['id_fuente']} ({row['id_especie']}.{row['campo']})")

    for row in species:
        species_id = row["id"]
        if not row["scientific_name_accepted"] or not row["aphia_id"]:
            errors.append(f"{species_id}: accepted scientific name and AphiaID are required")
        for field, value in row.items():
            if not value or field in STRUCTURAL_FIELDS:
                continue
            matches = source_map.get((species_id, field), [])
            if value not in matches:
                errors.append(f"{species_id}.{field}: populated value has no matching source record")
            if field in TEXT_FIELDS and SPANISH_MARKERS.search(value):
                errors.append(f"{species_id}.{field}: text appears to contain Spanish; use English")

        if row["depth_min_m"] and row["depth_max_m"]:
            if float(row["depth_min_m"]) > float(row["depth_max_m"]):
                errors.append(f"{species_id}: depth minimum exceeds maximum")
        if row["temperature_min_c"] and row["temperature_max_c"]:
            if float(row["temperature_min_c"]) > float(row["temperature_max_c"]):
                errors.append(f"{species_id}: temperature minimum exceeds maximum")

    if errors:
        print("Species validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Species validation passed ({len(species)} records; source links and required taxonomy present).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
