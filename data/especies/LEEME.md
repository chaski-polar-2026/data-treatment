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

## Remaining gaps

- No reviewed source states temperature optima; cachema min/max remain pending.
- Hake depth endpoints and seasonality remain blank; evidence supports a concentration interval, not species-wide limits.
- Scallop and octopus landings need a verified public species-level dataset.
- Continue to additional demersal and coastal species only after this pull request is accepted.

No bulk landing data were downloaded.
