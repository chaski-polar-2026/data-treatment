# data-treatment

Data download, preparation and statistical analysis behind **Chaski Polar**, our entry for the NASA Space Apps Challenge 2026 ("Be An Earth System Trend Detective!"). It studies associations between Southern Ocean variables, the Humboldt Current system and the Peruvian anchoveta (*Engraulis ringens*), 1998–2025.

- **Website and games (consumer of this analysis):** https://github.com/chaski-polar-2026/chaski-polar-webpage
- **Live site:** https://chaski-polar-2026-webpage.vercel.app

> Results are **exploratory associations**, not proof of causation or of physical transport between Antarctica and Peru. Across the preregistered tests, no robust Southern Ocean–Peru association survived the sensitivity checks.

## What is in this repository

| Folder | Content |
|---|---|
| `src/nasahackaton/` | Python package: data sources, downloads, transformations and models, plus the reference conditions monitor |
| `scripts/` | Numbered pipeline scripts (download → panels → experiments). `scripts/web_export/` holds the exporters that produce the JSON files used by the website |
| `analysis_r/` | Statistical pipeline in R (H0/H1 contrast); see `analysis_r/README.md` |
| `data/inputs/` | Small input snapshots with provenance and SHA-256 checksums, so results can be reproduced offline |
| `data/tablas_pruebas_pendientes/` | Confirmed result tables (they are not overwritten when reproducing) |
| `data/punto1_anchoveta/` | Landings, quotas and biomass, with one `LEEME.md` per source |
| `data/reproducciones/`, `data/web_export/` | Local outputs of reproduction runs, ignored by Git |
| `docs/` | Methodology, data notes, pipelines, reports, preregistrations (`docs/pruebas_pendientes/`) and the reproduction guide (`docs/REPRODUCIR.md`) |
| `tests/` | Automated tests |

## Set up

Python (requires [uv](https://docs.astral.sh/uv/); the project declares Python 3.14 or newer):

```bash
uv sync
uv run python scripts/<script>.py
```

R (4.x, only for `analysis_r/`):

```bash
Rscript analysis_r/00_install_packages.R
```

## How to reproduce and try it

The full guide is in [docs/REPRODUCIR.md](docs/REPRODUCIR.md). The runner does not download or install anything and does not touch the historical results.

Quick infrastructure check (PowerShell shown; set `PYTHONIOENCODING=utf-8` on any shell):

```powershell
$env:PYTHONIOENCODING = 'utf-8'
python scripts/reproducir_pruebas.py --rapido
```

- `--rapido` uses 100 permutation surrogates instead of the original 2000 in block 5. It is an **infrastructure test, not a result equivalent to the preregistration**; the functions and criteria are unchanged.
- Without `--rapido`, block 5 uses the original 2000 surrogates.
- Each run saves its log and tables under `data/reproducciones/` and writes a `comparacion.json` that compares the outputs with the committed reference (`IDENTICAL` means byte equality).
- The optional environment variable `CHASKI_DATA` changes only the root of the inputs (default `data/inputs/`).

To repeat only the exploratory models with the panel used in the report:

```bash
Rscript analysis_r/04_exploratory_models.R \
  --panel analysis_r/data/exploratory_nointerp/exploratory_cruise_panel_used.csv \
  --out-dir <output_folder>
```

`data/processed/` is not versioned, so intermediate panels must be regenerated with the scripts in `scripts/` before running the full pipeline.

## Documented results (summary)

- **Block 1:** none of the 896 tests passes FDR. Retrospective outlook and landings are described in [their report](docs/pruebas_pendientes/RESULTADOS_TELECONEXION_Y_PERSPECTIVA.md).
- **Long-term nutrients:** none of the 1200 tests meets the preregistered criterion; a null with this record does not demonstrate the absence of a slow link. [Report](docs/pruebas_pendientes/RESULTADOS_NUTRIENTES_LARGO_PLAZO.md).
- **Antarctica and neighbours:** leads are not presented as confirmed findings. [Report](docs/pruebas_pendientes/RESULTADOS_ANTARTIDA_VECINOS.md).
- **Altimetry and GLORYS** agree only partly; dependence and corrections limit the comparison. [Report](docs/pruebas_pendientes/RESULTADOS_ALTIMETRIA.md).

## Data for the website

The scripts in `scripts/web_export/` write into `data/web_export/`; they never write into the website repository. Verification reproduces `tendencias-ronda.json` and `nino-relaciones.json` exactly; `monitor-data.js` shows 2026/metadata differences that must be resolved before changing its calculation or publishing. To compare against the website data without writing into it:

```bash
python scripts/web_export/comparar.py --public-data <chaski-polar-webpage/public/assets/data>
```

## Sources

Each dataset states its source in its `LEEME.md` or in `docs/01_metodologia/metodologia.md`. Main sources: IMARPE (surveys and biomass), BCRP (landings), PRODUCE (quotas and seasons), RAM Legacy v4.44, NOAA PSL/CPC (Niño 1+2, PDO, AAO/SAM), NSIDC (Antarctic sea ice), ESA OC-CCI (chlorophyll), Copernicus Marine and World Ocean Atlas 2023. Source datasets keep the terms of their agencies.

## Limitations

See `docs/04_analisis/informe_analisis_exploratorio_h1_h0.md` (section 4.4). In short: few surveys with complete dates, results sensitive to the temporal structure, and biological responses that must not be combined with one another.

Scope of the variables:

- **Niño 1+2, temperature and chlorophyll** are the core of the analysis and feed the monitor and the game in the website repository.
- **Phytoplankton carbon** enters only as an exploratory response (`ab_phytoplankton_carbon`) and is not mixed with chlorophyll.
- **Temperature and oxygen at 100–200 m** have a trend round in `docs/pruebas_pendientes/RESULTADOS_RONDA_SEIS_VARIABLES.md`; they are not yet used in the monitor or the game.

## Team and license

- S. Nikol A. Solaligue Limache, Ariana Cardenas Huaman, Aroon A. Delgado Huaychani and Denis Quispe Condori (roles are listed on the website's About page).
- **Code:** [MIT License](LICENSE). Texts, tables and processed datasets: CC BY 4.0 (credit the Chaski Polar team). Source datasets keep their agencies' terms.
- AI assistants (OpenAI Codex, Anthropic Claude Code) supported code refactoring, verification scripts and drafting. No AI or machine-learning model is part of the results.
