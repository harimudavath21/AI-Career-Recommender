"""
Build CareerCompass AI's occupation catalogue from the official ESCO CSV export.

Expected input:
    D:\\hackathon\\data\\esco\\
        occupations*.csv
        skills*.csv (or skill*.csv)
        occupationSkillRelations*.csv

Run:
    python scripts\\import_esco.py --input data\\esco

The script supports common ESCO CSV header variants and writes:
    data\\occupation_profiles.json

Download ESCO CSV classification files from:
https://esco.ec.europa.eu/en/use-esco/download
Choose the latest version, Classification, English, CSV.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import pandas as pd


def read_csv_safely(path: Path) -> pd.DataFrame:
    """Read ESCO CSVs with delimiter and encoding fallbacks."""
    for encoding in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            return pd.read_csv(path, sep=None, engine="python", encoding=encoding)
        except Exception:
            continue
    raise RuntimeError(f"Could not read CSV file: {path}")


def norm(value: object) -> str:
    return re.sub(r"[^a-z0-9]+", "", str(value).lower())


def find_column(df: pd.DataFrame, candidates: list[str]) -> str | None:
    normalized = {norm(column): column for column in df.columns}
    for candidate in candidates:
        if norm(candidate) in normalized:
            return normalized[norm(candidate)]
    for column in df.columns:
        col_norm = norm(column)
        if any(norm(candidate) in col_norm for candidate in candidates):
            return column
    return None


def locate_csv(folder: Path, tokens: list[str]) -> Path:
    candidates = sorted(folder.rglob("*.csv"))
    matches = [
        path for path in candidates
        if all(token in norm(path.stem) for token in tokens)
    ]

    # Prefer the actual concept tables, not relation/group/collection tables.
    if tokens == ["occupation"]:
        matches = [
            path for path in matches
            if "relation" not in norm(path.stem)
            and "group" not in norm(path.stem)
            and norm(path.stem).startswith("occupation")
        ]
    elif tokens == ["skill"]:
        matches = [
            path for path in matches
            if "relation" not in norm(path.stem)
            and "group" not in norm(path.stem)
            and "collection" not in norm(path.stem)
            and norm(path.stem).startswith("skill")
        ]
    elif tokens == ["occupationskillrelation"]:
        matches = [
            path for path in matches
            if "relation" in norm(path.stem)
        ]

    if matches:
        return matches[0]
    raise FileNotFoundError(
        f"Could not find CSV matching {tokens}. "
        f"CSV files found: {[p.name for p in candidates[:30]]}"
    )


def clean_list(values: list[str]) -> list[str]:
    return sorted({v.strip() for v in values if isinstance(v, str) and v.strip()})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/esco", help="Folder containing ESCO CSV files")
    parser.add_argument("--output", default="data/occupation_profiles.json")
    args = parser.parse_args()

    input_dir = Path(args.input).resolve()
    output_path = Path(args.output).resolve()

    occupations_path = locate_csv(input_dir, ["occupation"])
    skills_path = locate_csv(input_dir, ["skill"])
    relations_path = locate_csv(input_dir, ["occupationskillrelation"])

    occupations = read_csv_safely(occupations_path)
    skills = read_csv_safely(skills_path)
    relations = read_csv_safely(relations_path)

    occ_uri_col = find_column(occupations, ["conceptUri", "occupationUri", "uri"])
    occ_title_col = find_column(occupations, ["preferredLabel", "conceptPT", "preferredTerm", "label"])
    occ_desc_col = find_column(occupations, ["description", "definition"])
    occ_type_col = find_column(occupations, ["conceptType", "type"])
    occ_code_col = find_column(occupations, ["iscoGroup", "iscoCode", "code"])
    occ_alt_col = find_column(occupations, ["altLabels", "alternativeLabel", "alternateLabels"])

    skill_uri_col = find_column(skills, ["conceptUri", "skillUri", "uri"])
    skill_title_col = find_column(skills, ["preferredLabel", "conceptPT", "preferredTerm", "label"])

    rel_occ_col = find_column(relations, ["occupationUri", "occupationConceptUri", "conceptUri"])
    rel_skill_col = find_column(relations, ["skillUri", "skillConceptUri", "relatedSkillUri"])
    rel_type_col = find_column(relations, ["relationType", "type"])

    required = {
        "occupation URI": occ_uri_col,
        "occupation title": occ_title_col,
        "skill URI": skill_uri_col,
        "skill title": skill_title_col,
        "relation occupation URI": rel_occ_col,
        "relation skill URI": rel_skill_col,
    }
    missing = [name for name, col in required.items() if col is None]
    if missing:
        raise ValueError(
            "Could not identify required ESCO columns: " + ", ".join(missing) +
            f"\nOccupation columns: {list(occupations.columns)}" +
            f"\nSkill columns: {list(skills.columns)}" +
            f"\nRelation columns: {list(relations.columns)}"
        )

    # ESCO concept types distinguish occupation groups (OG) from occupations (OC).
    if occ_type_col:
        types = occupations[occ_type_col].astype(str).str.upper()
        occupations = occupations[types.isin(["OC", "OCCUPATION", "NAN"])].copy()

    skill_lookup = {}
    for _, row in skills.iterrows():
        uri = str(row[skill_uri_col]).strip()
        label = str(row[skill_title_col]).strip()
        if uri and label and label.lower() != "nan":
            skill_lookup[uri] = label

    relation_map: dict[str, dict[str, float]] = {}
    for _, row in relations.iterrows():
        occ_uri = str(row[rel_occ_col]).strip()
        skill_uri = str(row[rel_skill_col]).strip()
        skill_label = skill_lookup.get(skill_uri)
        if not occ_uri or not skill_label:
            continue

        relation_type = str(row[rel_type_col]).lower() if rel_type_col else ""
        # Essential skills receive higher relative weight than optional skills.
        weight = 1.0 if "essential" in relation_type else 0.65
        relation_map.setdefault(occ_uri, {})[skill_label] = max(
            weight, relation_map.setdefault(occ_uri, {}).get(skill_label, 0)
        )

    profiles = {}
    for _, row in occupations.iterrows():
        uri = str(row[occ_uri_col]).strip()
        title = str(row[occ_title_col]).strip()
        if not uri or not title or title.lower() == "nan":
            continue

        occupation_skills = relation_map.get(uri, {})
        if not occupation_skills:
            continue

        description = ""
        if occ_desc_col and pd.notna(row[occ_desc_col]):
            description = str(row[occ_desc_col]).strip()

        category = "Other Occupations"
        if occ_code_col and pd.notna(row[occ_code_col]):
            category = f"ISCO {str(row[occ_code_col]).strip()}"

        alternate_labels = []
        if occ_alt_col and pd.notna(row[occ_alt_col]):
            alternate_labels = re.split(r"[,;|]", str(row[occ_alt_col]))
            alternate_labels = clean_list(alternate_labels)

        profiles[title] = {
            "category": category,
            "skills": occupation_skills,
            "projects": [],
            "education": [],
            "description": description,
            "source": "ESCO",
            "uri": uri,
            "alternate_labels": alternate_labels,
        }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "metadata": {
            "source": "European Commission ESCO",
            "dataset_version": "v1.2.1 (verify against downloaded package)",
            "occupation_count": len(profiles),
            "skill_concept_count": len(skill_lookup),
            "generated_from": [
                str(occupations_path.name),
                str(skills_path.name),
                str(relations_path.name),
            ],
        },
        "occupations": profiles,
    }
    output_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Imported {len(profiles):,} occupations with linked skills.")
    print(f"Loaded {len(skill_lookup):,} ESCO skill concepts.")
    print(f"Saved catalogue to: {output_path}")


if __name__ == "__main__":
    main()
