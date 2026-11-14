"""Descarga únicamente SLA mensual en la caja peruana mediante Copernicus Marine."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import copernicusmarine

DATASET = 'c3s_obs-sl_glo_phy-ssh_my_twosat-l4-duacs-0.25deg_P1M-m'
PRODUCT = 'SEALEVEL_GLO_PHY_CLIMATE_L4_MY_008_057'
VERSION = '202411'


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--raw-dir', type=Path, default=Path('/tmp/anchoveta_altimetria'))
    p.add_argument('--force', action='store_true')
    a = p.parse_args()
    a.raw_dir.mkdir(parents=True, exist_ok=True)
    target = a.raw_dir / 'sla_peru_1993_2025.nc'
    if target.exists() and not a.force:
        raise SystemExit(f'Ya existe {target}; usa --force para reemplazarlo.')
    copernicusmarine.subset(dataset_id=DATASET, dataset_version=VERSION, variables=['sla'], minimum_longitude=-85,
        maximum_longitude=-70, minimum_latitude=-18.35, maximum_latitude=-3.38,
        start_datetime='1993-01-01', end_datetime='2025-12-01',
        output_directory=str(a.raw_dir), output_filename=target.name, overwrite=a.force)
    import xarray as xr
    with xr.open_dataset(target) as ds:
        metadata = {'global': {k: str(v) for k, v in ds.attrs.items()},
                    'sla': {k: str(v) for k, v in ds['sla'].attrs.items()}}
    manifest = {'product': PRODUCT, 'dataset_id': DATASET, 'version': VERSION,
        'downloaded_utc': datetime.now(timezone.utc).isoformat(), 'bbox': [-85, -18.35, -70, -3.38],
        'period': ['1993-01-01', '2025-12-31'], 'variable': 'sla', 'file': str(target.resolve()),
        'sha256': hashlib.sha256(target.read_bytes()).hexdigest(), 'metadata': metadata,
        'documentation': 'https://documentation.marine.copernicus.eu/PUM/CMEMS-SL-PUM-008-057.pdf'}
    (a.raw_dir / 'manifest.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'Descargado: {target}; manifiesto: {a.raw_dir / "manifest.json"}')

if __name__ == '__main__':
    main()
