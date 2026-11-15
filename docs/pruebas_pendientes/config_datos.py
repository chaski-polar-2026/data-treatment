"""Portable paths. Only CHASKI_DATA configures inputs; never writes to originals."""
import os
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
DATA = Path(os.environ.get('CHASKI_DATA', ROOT / 'data/inputs')).expanduser().resolve()
# Outputs are always isolated from committed results, including direct script runs.
OUTPUT = ROOT / 'data/reproducciones'
TABLES = OUTPUT / 'data/tablas_pruebas_pendientes'
TABLES.mkdir(parents=True, exist_ok=True)
DOCS = OUTPUT / 'docs/pruebas_pendientes'
DOCS.mkdir(parents=True, exist_ok=True)
WEB_EXPORT = ROOT / 'data/web_export'
WEB_EXPORT.mkdir(parents=True, exist_ok=True)

def require(relative):
    path = DATA / relative
    if not path.is_file():
        raise FileNotFoundError(f'Missing input: {relative}. Place it under CHASKI_DATA (default data/inputs). See data/inputs/LEEME.md; no automatic download.')
    return path
