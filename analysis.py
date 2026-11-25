"""Build a matched-economy comparison of World Development Indicators port traffic."""
import json
from math import isfinite
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parent
YEARS = list(range(2019, 2025))
INDICATOR = "IS.SHP.GOOD.TU"


def read_response(path):
    metadata, rows = json.loads(path.read_text(encoding="utf-8-sig"))
    if int(metadata["pages"]) != 1 or len(rows) != int(metadata["total"]):
        raise ValueError(f"Incomplete API snapshot: {path.name}")
    return metadata, rows


def economy_panel(geography, observations):
    # World Bank economies can include territories. Region NA denotes aggregate rows.
    by_code = {
        row["id"]: {"code": row["id"], "name": row["name"], "region": row["region"]["value"].strip(),
                    "values": dict.fromkeys(YEARS)}
        for row in geography if row["region"]["id"] not in ("NA", "")
    }
    seen = set()
    for row in observations:
        code, year = row["countryiso3code"], int(row["date"])
        if row["indicator"]["id"] != INDICATOR or year not in YEARS:
            raise ValueError(f"Unexpected observation: {code} {year}")
        if code not in by_code:
            continue
        key = (code, year)
        if key in seen:
            raise ValueError(f"Duplicate observation: {key}")
        seen.add(key)
        value = row["value"]
        if value is not None and (isinstance(value, bool) or not isinstance(value, (float, int))
                                  or not isfinite(value) or value < 0):
            raise ValueError(f"Invalid throughput: {key}")
        by_code[code]["values"][year] = value
    return sorted(by_code.values(), key=lambda r: (r["name"].casefold(), r["code"]))


def paired_summary(rows, year):
    pairs = [(row["values"][2019], row["values"][year]) for row in rows]
    matched = [(base, new) for base, new in pairs if base is not None and base > 0 and new is not None]
    base_total = sum(base for base, _ in matched)
    new_total = sum(new for _, new in matched)
    return {
        "eligible": len(rows), "observed": sum(new is not None for _, new in pairs),
        "missing": sum(new is None for _, new in pairs), "paired": len(matched),
        "baseline": base_total, "comparison": new_total,
        "combined_change": round(100 * (new_total-base_total)/base_total, 6) if base_total else None,
        "median_change": round(median(100*(new-base)/base for base, new in matched), 6) if matched else None,
    }


def experiment():
    metadata, observations = read_response(ROOT / "source-data/traffic.json")
    _, geography = read_response(ROOT / "source-data/economies.json")
    rows = economy_panel(geography, observations)
    return {
        "years": YEARS, "updated": metadata["lastupdated"], "snapshot": "2026-11-25",
        "regions": sorted({row["region"] for row in rows}), "economies": rows,
        "coverage": {year: paired_summary(rows, year) for year in YEARS},
    }
