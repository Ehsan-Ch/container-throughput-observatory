# Container Throughput Observatory

An economy-level analysis of container-port throughput using World Development Indicators. Compare any year from 2020 through 2024 against 2019, filter by region, inspect annual trends, and export matched, all, or missing economies.

[Open the interactive report](https://ehsan-ch.github.io/container-throughput-observatory/)

## Results

The snapshot has a 2024 value for **103 of 217** eligible economies. **100** have both a 2024 observation and a positive 2019 baseline. Within that paired set, summed throughput rose from **776.6 million to 896.3 million TEU (+15.4%)**. The median economy grew **8.7%**. The combined and median changes differ because larger economies have more weight in the combined measure. There are **114** eligible economies with no 2024 observation. These include economies with no observations during the period and may include economies without seaports.

## Reproduce

Run `python build.py` followed by `python -m unittest -v` with Python 3.12. Open `index.html` directly. No external packages or network access are required to reproduce the frozen report.

The bundled snapshots were retrieved on 25 November 2026. The indicator response reports an upstream update date of 11 November 2026. The original queries were:

- [WDI traffic observations, 2019–2024](https://api.worldbank.org/v2/country/all/indicator/IS.SHP.GOOD.TU?source=2&date=2019:2024&format=json&per_page=2000). SHA-256 `f1f9ebd22b6b5a2ec05911839d8bf186d379b28e2d7c6a53f4aea57f24bd6f07`.
- [World Bank economy metadata](https://api.worldbank.org/v2/country?format=json&per_page=400). SHA-256 `c9acf3932785191a649cbc04c3056af4cf64a236e5c3b49d49be25ddb0440bce`.

## Method and limits

Join the two responses by three-character economy code. Exclude aggregate geographies identified by the API metadata. Keep all 217 remaining economies, including territories, and preserve missing observations as null. For each comparison year, require positive 2019 throughput and a nonmissing comparison value. The UI recomputes both aggregate and median changes for the active region and year. The record filter and sorting affect the table and CSV rather than the summary. The screen displays up to 25 rows and the export includes the entire selection.

The 2019 cohort is re-matched for every comparison year. Missingness is substantial and can be selective. Combined throughput is for the matched reporting subset, not a regional or global total. The indicator measures port activity in TEU, which can include transshipment. It cannot be used as a count of unique trade shipments or cargo value.

## Data attribution

UN Conference on Trade and Development (UNCTAD), via World Bank World Development Indicators, [container port traffic, IS.SHP.GOOD.TU](https://data.worldbank.org/indicator/IS.SHP.GOOD.TU). The indicator page identifies the source and [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). See the [World Bank dataset terms](https://www.worldbank.org/ext/en/legal/terms-conditions/datasets). The derived comparison and presentation are project calculations. The MIT license covers project code.
