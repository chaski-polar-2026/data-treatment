# Priority species data: review update

This first batch covers anchoveta, jumbo flying squid, Peruvian scallop, Peruvian octopus, Peruvian hake, and cachema. Populated ecological values have a source, locator, and short excerpt in `especies_fuentes.csv`; empty values mean no verifiable evidence was found.

## Review decisions

- **Jumbo flying squid depth:** the 2018 IMARPE article has different depth wording in its Spanish and English abstracts. The 1200 m maximum is supported independently by Sakai et al. (2017), page 174: two tagged squid reached that depth. It is a sample observation, not a population limit.
- **Scallop depth:** IMARPE thesis section 2.7.2, page 12, reports typical habitat at 5-40 m. The IMARPE species sheet gives a broader intertidal-to-95 m distribution; the narrower range describes typical habitat.
- **WoRMS:** Aphia REST confirms *Cynoscion analis* (276076) and *Merluccius peruanus* (1524920) as accepted species. *Merluccius gayi peruanus* is recorded as the hake synonym.
- **Temperature:** values are field observations or lab treatments, not tolerance limits. None of the reviewed sources stated an optimum, so optimum fields are empty. Cachema min/max/optimum remain empty because the available temperature observations were ambiguous.
- **Landings:** PRODUCE provides a public anchovy register. The GORE Piura monthly species-by-port dataset lists pota, merluza, and cachema (regional coverage; fleet class is not specified per record). No verified species-level landing dataset was found for scallop or octopus. The catalogue preview was checked; no bulk data were downloaded.

## Random spot check

Using seed `20261115`, 8 of 80 sourced field values (10%) were selected and checked against the linked source and locator. **8 confirmed; 0 unconfirmed:** scallop maximum temperature, anchoveta minimum depth, hake minimum temperature, squid maximum depth, octopus AphiaID, squid maximum temperature, hake accepted name, and squid spawning season. The WoRMS taxon page HTML returned an access error to the automated browser; the public Aphia REST records confirmed accepted names and AphiaIDs.

## How to read the ranges

Recorded values describe the records cited here. They are not tolerance limits, preferred ranges or evidence of catch likelihood. A comparison flag does not establish that any environmental measurement is suitable for comparison: depth, place and measurement context must match.

- `field_seasonal_observation`: seasonal field temperatures. `temperature_comparable` may be true for a comparison in the same measurement context.
- `field_depth_mixed_observation`: observations from different depths. The squid values combine 50 m and surface observations; comparison is disabled.
- `bottom_temperature_cruise`: bottom temperatures recorded during cruises. Compare only with bottom measurements in the same context, not sea-surface temperature.
- `laboratory_treatment`: experimental treatment temperatures. They do not define a field range; comparison is disabled.
- `distribution_range`: a depth range described by the cited distribution record. It is not a tolerance limit.
- `dive_depth_observation`: a recorded dive. The squid maximum comes from two tagged animals, not a species-wide endpoint. The web label is "Deepest recorded dive".
- `survey_stratum`: a depth band sampled by a survey, not the limits of a species. No current record uses this basis.

The new columns classify existing notes and quotes. They do not add new measurements or sources. Empty metadata means no range is recorded. JSON groups temperatures under `recorded_temperature` and depths under `recorded_depth`. CSV numerical columns retain their existing values.

## Remaining gaps

- No reviewed source states temperature optima; cachema min/max remain pending.
- Hake depth endpoints and seasonality remain blank; evidence supports a concentration interval, not species-wide limits.
- Scallop and octopus landings need a verified public species-level dataset.
- Continue to additional demersal and coastal species only after this pull request is accepted.

No bulk landing data were downloaded.

## Priority-1 completion review (2026-11-15)

Five new cited field values were added: cachema depth endpoints (0 and 50 m; F24, section Cynoscion analis / Figure 6), hake minimum depth (50 m), an open-ended depth note, and spawning season (F25, printed p. 49). All prior nonempty ecological values, source rows, quotes and consultation dates are retained. Administrative review status is appended after ` Review status:` in notes; only the original sourced prefix is checked as a quoted ecological value. New fields `depth_note` and `temperature_optimum_note` require citations when populated. Basis columns classify the cited text, not new measurements.

The hake guide states more than 600 m. `depth_max_m` stays empty; 600 must not become a closed endpoint. Its basis is distribution_range, not survey_stratum: the added evidence describes habitat rather than survey sampling bands. The pre-existing 100–200 m concentration statement remains in habitat_summary and is not used as distribution endpoints. The 2022 IMARPE assessment introduction also describes 50 to more than 600 m: https://cdn.www.gob.pe/uploads/document/file/3497401/Informe%20Cuota%20merluza%20julio%202022%20-%20junio%202023.pdf . A search candidate for the 2025 assessment describes 50–500 m, but opening it returned 418: **no accesible**. This is a pending possible discrepancy, not a verified correction. No confirmed contradictory new values were selected; mark sources_disagree if the candidate is verified later. The older scallop depth discrepancy (5–40 m versus a broader record) remains documented above; neither value was changed.

### Thermal optimum search and pending work

Every optimum stays empty. Notes record "No thermal optimum reported in reviewed sources"; this describes this review, not proof that none exists. Experimental treatment temperatures, model outputs and study-specific intervals were not converted into a species-wide optimum.

| Species | Review outcome / next source to inspect |
|---|---|
| Anchoveta | No explicit numerical experimental optimum verified. FishBase candidate https://www.fishbase.se/Country/CountrySpeciesSummary.php?c_code=604&id=4 appeared in search only; thermal-preference provenance remains pending. |
| Pota | Review DOI 10.3989/scimar.04497.25B describes regional feeding/spawning intervals, not a single experimental optimum. Chesney et al. (2013), discussion, https://calcofi.org/downloads/publications/calcofireports/v54/Vol_54_Chesney.pdf cites a daytime preference range outside Peru; no point optimum was inferred. Follow the primary experiment before adding a study-scoped preference. |
| Pulpo | Thermoregulatory behavior and oxygen consumption of Octopus mimus paralarvae: The effect of age, https://www.sciencedirect.com/science/article/abs/pii/S0306456512001520 : **no accesible**, HTTP 403. Search snippets alone were not accepted. A paralarval result cannot be generalized to adults. |
| Scallop | DOI 10.3390/fishes9010009 accessed: Chilean broodstock conditioning treatments, not a stated species-wide optimum. DOI 10.1016/S0044-8486(03)00321-1 and https://www.sciencedirect.com/science/article/abs/pii/S0044848699002914 : **no accesible**, HTTP 403. |
| Hake | IMARPE guide verified for depth and season, not an optimum. FAO catalogue front matter https://www.fao.org/4/y4876e/y4876e.pdf opened, but no species-specific optimum verified in it. |
| Cachema | No explicit optimum verified. The mixed-column PDF https://repositorio.imarpe.gob.pe/bitstream/20.500.12958/2166/1/INF%2038%283%29-10.pdf needs visual checking: search/extracted text interleaves species. Temperature endpoints stay pending, not assigned from adjacent text. |

The validator now requires both an optimum study note and matching sourced quotes for a populated optimum. An independent experimental optimum is not required to lie inside recorded field endpoints: observations are not tolerance limits. The JSON export retains the prior rule excluding optimum/preferred/suitability fields; publishing a future experimental optimum needs a separate, study-scoped export design.

### Source access and existing notes

- Cachema F17: **no accesible**, HTTP 502; its existing season and El Nino notes and citations are retained, not marked newly verified.
- Anchoveta F11 and F2: **no accesible**, timeout. Pota F12: **no accesible**, timeout; F22: **no accesible**, HTTP 502. Both existing season and El Nino fields already have citations; none was filled from memory.
- Pulpo F15 opened: diet section pp. 2–3 distinguishes Pisco 1982–83 and Pucusana 1997–98; the existing response note is retained. The same sheet reports site-specific spawning peaks. F13 for the existing Ancash season: **no accesible**, HTTP 502; no replacement with a different location was made.
- Scallop F14: **no accesible**, timeout; F23: **no accesible**, HTTP 502. Existing season and response are retained with their sources, pending a new full-text check.
- Direct Python PDF requests failed certificate verification; verification was not disabled. Web text access worked for F24/F25/F26; screenshot attempts for the cachema cruise and hake guide timed out. No local PDF was accepted or executed.

### Landings catalogue

The public IMARPE April 2023 report (F26), Figure 51(c)/(d), opens without a session and contains monthly pulpo/scallop charts for January 2022–April 2023, grouped by landing ports. Those catalogue rows now identify this report and its preliminary artisanal-monitoring context. They do not assert a downloadable dataset or fleet class for individual records. Species landing_data_* fields remain empty and landings_pending remains set because a machine-readable species-level endpoint was not verified. No totals were digitized from figures, and no bulk landing data were downloaded.

The Piura open-data endpoint already recorded as F19 returned HTTP 403 (**no accesible**). The public IMARPE service landing page https://www.gob.pe/12280-consultar-el-reporte-de-la-actividad-pesquera returned HTTP 418 (**no accesible**). Registration was not attempted. Denis should verify an open species-level dataset, its years, geographic coverage and fleet definition before replacing the report-only catalogue entries.

### New random spot check

Seed 20261115; population: five newly cited species-field values, in appended CSV order. Sample size: ceil(10% × 5) = 1 (20% after rounding). Selected: merluza.depth_min_m = 50; F25, printed p. 49, habitat. Reopening the web PDF text confirms the passage "desde 50 m a más de 600 m de profundidad". **1 confirmed, 0 unconfirmed.** This checks the lower endpoint only; no closed maximum is inferred. The earlier eight-value random check above is unchanged.

### Remaining gaps after this review

- Cachema temperature: ambiguous species attribution in extracted text; verify the original page visually. Existing season/El Nino notes need renewed access to F17.
- Hake upper depth: open-ended in the verified guide; inspect the inaccessible 2025 candidate before resolving any discrepancy. Season is now sourced.
- All six experimental thermal optima: pending explicit, accessible study results with life stage, location and method. Do not fill from treatment temperatures or inferred habitat ranges.
- Scallop and pulpo landings: a regional machine-readable CSV exists (GORE Piura / DIREPRO, species "Concha de abanico" and "Pulpo" seen in a partial read, 2026-11-15; Piura only). National species-level machine-readable data remain pending; the IMARPE report charts (F26) are not a raw dataset.
- Cachema temperature: FishBase species page 403 (F27, read 2026-11-15) has no temperature line, so the field stays empty. Do not use a model-based estimate without a verified source page.
- Optional OBIS/GBIF presence counts were not collected; no environmental conditions were extracted.

Existing differing source descriptions for squid depth wording and scallop depth coverage are now flagged `sources_disagree`; their original notes and references are retained. No new endpoint was chosen to resolve those differences.


## Review completed 2026-11-15
Six new species records: bonito, perico, jurel, caballa, lorna and corvina. All six accepted scientific names and Aphia IDs were verified through the public WoRMS REST API. The records remain partial in biological coverage: empty fields mean no sufficiently verified evidence, not absence of the phenomenon. No capture forecast is implied.

### Remaining field gaps and decisions
- All six new temperature ranges: left blank. Jurel and caballa factsheets give general environmental ranges without the required observation basis. Caballa also states a preferred range but does not identify life stage or study method; no scalar optimum was invented.
- Bonito: verified depth, habitat, spawning, diet during El Nino, coast range and fishery; temperature and accessible landings series unresolved.
- Perico: verified depth, habitat, coast range and fishery; seasonal and El Nino fields unresolved in the imported evidence. February 2010 IMARPE report table 17 contains survey-wide surface temperatures, not a demonstrated species-specific thermal range, so these were not imported.
- Jurel: verified taxonomy, habitat, spawning and fishery. Closed depth bounds and coast-specific range remain blank.
- Caballa: verified taxonomy, habitat, upper depth, coast range and fishery. Lower depth, spawning and species-specific El Nino response remain blank.
- Lorna: Callaus deliciosa is accepted, not a spelling error. WoRMS returns authority Jordan, 1889, while IMARPE prints Tschudi, 1846; authority is not part of the accepted-name field and this discrepancy remains unresolved. The autumn spawning peak in the factsheet differs from the spring 1996 Huacho observation; both sources are retained with sources_disagree.
- Corvina: verified taxonomy, habitat, upper depth, coast range and fishery. Lower depth, spawning, temperature and El Nino response remain blank.
- Cachema: IMARPE summer 2003 report (https://repositorio.imarpe.gob.pe/bitstream/20.500.12958/2234/1/Informe%2039%283-4%2912.pdf) explicitly mentions a minimum of 19.2 C. Its multicolumn text extraction interleaves species and upper endpoints; visual page access failed, so no min/max pair was assigned. Laboratory hormone study table 1 (https://revistas.untumbes.edu.pe/index.php/manglar/es/article/download/99/113/387) was also reviewed; it is not a thermal-treatment study and was not forced into that basis.
- Merluza: added published upper capture depth 800 m from F41, p. 249. This is a source-specific recorded extent, not a physiological limit. The original 50 m lower bound and guide note are preserved; the sources describe different scopes.
- Thermal optima: no new optimum imported for the original six. Octopus mimus thermoregulation paper was located, but publisher access returned 403; secondary reports of 22.8 C were not used as primary evidence. Searches for the other five did not establish a directly verified optimum with study context. This does not prove that such studies do not exist.
- Landing sources: three open PDF report entries added for lorna, corvina and caballa. These are report summaries, not machine-readable series; landing_data fields remain blank and landings_pending remains set. No bulk data downloaded.
- Other coastal species and invertebrates in the candidate list were not added; the six-species minimum determines this delivery's scope.

### Access log
No accesible: WoRMS individual HTML records (403); public REST API succeeded for all six. IMARPE bonito PDF timed out in web tool; direct HTTPS download succeeded. IMARPE repository direct Python reads failed certificate verification; web-reader copies were used where available, without disabling TLS verification. Cachema review page timed out; Lambayeque El Nino 2017 item returned 502. FishBase corvina returned 403 and mirror cache miss. PRODUCE lorna page and Piura open-data CSV returned 418. Perico 2021 annual report returned 403. ScienceDirect hake and octopus articles returned 403; an open scholarly copy of the hake paper was read. No authentication or block evasion was used.

### Audit
Seed 20261115; 61 distinct new sourced field values; sample ceil(10%) = 7. Sources were downloaded again after sampling. Confirmed 7/7; unconfirmed 0. Sample: caballa/common_name_es; jurel/common_name_es; bonito/fishery_note; lorna/depth_min_m, group, depth_max_m, common_name_es. See RESUMEN_CAMBIOS.md for validation and packaging results.

## Second completion review (2026-11-15)

This review covers jurel, perico, caballa, bonito, lorna, corvina and cachema, plus landing datasets for scallop and octopus. The CSV actually has 28 columns; its existing column names and order are preserved. Python `csv` writes text fields with LF line endings; no numeric conversion is used.

### New observations and their scope

- **Jurel, F43:** recorded schools span 0-75 m during strong upwelling, 100-200 m during strong El Nino, and 0-300 m with a stronger southern Cromwell extension (Dioses 2013, p. 67). The new depth endpoints describe the broadest reported distribution pattern, not species limits or the 0-180 m survey sampling grid. Catches below 100 m during El Nino were recorded at 15-20 C (p. 68); `field_depth_mixed_observation` is used because this summary spans depth levels rather than a seasonal surface series, and comparison is disabled. No optimum is inferred.
- **Lorna and cachema, F42:** bottom-trawl cruise temperatures from northern Peru, 1981-1988, use `bottom_temperature_cruise` and `temperature_comparable=true`; comparison still requires matching bottom depth and setting. The scalar endpoints describe normal years only: lorna 14.1-16.7 C and cachema 14.2-17.2 C. The temperature notes separately give El Nino records of 14.8-21.2 C and 16.3-22.4 C. Methods are on p. 4, species text on p. 5, and Table 1 on p. 12; the scanned table was also inspected visually.
- **Depth disagreements, F42 versus F37/F24/F27:** keep lorna's existing 5-50 m and cachema's existing 0-50 m unchanged. Add separate cited depth records: lorna 140 m in normal years and 222 m during El Nino; cachema 165 m and 154 m respectively. Both species retain `sources_disagree`; the new observations do not prove that the existing distribution sources are erroneous. Lorna's new depth note explains the different settings; cachema's existing depth note remains unchanged.
- **Perico, F45:** spring/summer describes higher artisanal landings, not spawning. High historical landings in 1983, 1987 and 1998 are linked to El Nino in section 3.1 (PDF p. 6); this does not establish a change in stock size.
- **Caballa, F44/F47:** the main reproductive period is November-March, with a January historical peak (F44, section 4.2). The new El Nino note describes local summer landings and equatorial surface waters in Lambayeque in 2015, not a stock-size response (F47, resource-environment section, caballa paragraph following Figure 28).

Every existing nonempty scientific value, source, excerpt and consultation date is retained. The sole replaced scientific review text is cachema's obsolete `notes` prefix saying no temperature range was verified: F42 now supplies a clear species-attributed passage, so a newly cited note replaces that status; the old note and citation remain in Git and the original citation row is retained. New source IDs are F42-F47; F46 records the open landing workbook reviewed in this task. No new optimum is entered, and no tolerance or catch claim is inferred.

### Downloadable landing catalogue

F46 is the PRODUCE Observatorio workbook [BD_PA_2013-2025-dic.xlsx](https://www.producempresarial.pe/wp-content/uploads/2024/01/BD_PA_2013-2025-dic.xlsx), linked from its [catalogue page](https://www.producempresarial.pe/desembarque-pesquero-artesanal-2013-2023/). Both opened without login: the workbook returned HTTP 200 for HEAD and 206 for partial byte requests. Only its ZIP directory, shared strings and first 3982 worksheet rows were read (about 0.23 MB transferred, rather than the 9.97 MB file); no landing values were copied into the species table. The catalogue period is 2013-2025, monthly, by region and landing point across Peru, not proof of continuous coverage for every species.

Sheet `BD`, row 5, has year, month, use, region, landing point, environment, species and tonnes. Maritime examples verified: PERICO row 7; BONITO 15; PULPO 30; CABALLA 66; JUREL 149; LORNA 200; CORVINA 361. `desembarques_disponibles.csv` gains seven entries, and matching source/locator/excerpt rows document each metadata field. The seven records now link an open downloadable catalogue, so `landings_pending` is removed for that completed catalogue task; scientific-name mapping and continuous annual coverage still need review. CORVINA also occurs in continental rows: restrict `AMBITO` to `MARITIMO` and do not equate the freshwater fish with Cilus gilberti. The workbook uses common names without scientific IDs, and its footnote describes estimates using the type of use and larger-vessel discharge records; it is not a raw trip register with a verified fleet for every row.

Cachema's existing Piura source is unchanged: the national workbook has AYANQUE, but its scientific-name mapping was not verified here. No CONCHA DE ABANICO label occurs in the full shared-string table (CONCHA NEGRA is a different label); no national scallop dataset is claimed. Existing Piura and IMARPE report entries for scallop and octopus remain intact. The new national octopus entry supplies the previously missing downloadable catalogue, with the scope limits above. Species CSV checkout line endings are fixed to LF in `.gitattributes`.

The four alternate cruise depth maxima use `campo=depth_max_m_alternative` in the citation table. They therefore appear as separate evidence in JSON and do not attach a 165 m or 222 m excerpt as support for the unchanged 50 m endpoint. This does not add or replace a column in `especies.csv`.
