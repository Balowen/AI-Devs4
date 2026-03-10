"""
Step 1: Load people.csv and filter by:
  - gender == "M"
  - birthPlace == "Grudziądz"
  - age in 2026 between 20 and 40 (inclusive)  =>  born in 1986..2006
"""
import csv
import json
from pathlib import Path

CSV_PATH = Path(__file__).parent.parent / "input" / "people.csv"
OUTPUT_DIR = Path(__file__).parent.parent / "output"
CURRENT_YEAR = 2026
MIN_AGE = 20
MAX_AGE = 40


def birth_year(birth_date: str) -> int:
    """Parse YYYY-MM-DD and return year."""
    return int(birth_date.split("-")[0])


def step_filter_people(output_dir: Path) -> list[dict]:
    """Load CSV, filter by criteria, save to output/filtered_people.json, return list.
    If filtered_people.json already exists, load and return it (skip filtering).
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / "filtered_people.json"

    if out_path.exists():
        with open(out_path, encoding="utf-8") as f:
            filtered = json.load(f)
        print(f"  Using cached filter result: {len(filtered)} persons ← {out_path}")
        return filtered

    filtered = []
    with open(CSV_PATH, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["gender"] != "M":
                continue
            if row["birthPlace"] != "Grudziądz":
                continue
            year = birth_year(row["birthDate"])
            age_in_2026 = CURRENT_YEAR - year
            if not (MIN_AGE <= age_in_2026 <= MAX_AGE):
                continue
            # Output in final answer shape; keep "job" for step 2 (tagging)
            filtered.append({
                "name": row["name"],
                "surname": row["surname"],
                "gender": row["gender"],
                "born": year,
                "city": row["birthPlace"],
                "tags": [],
                "job": row["job"],
            })

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(filtered, f, ensure_ascii=False, indent=2)
    print(f"  Filtered: {len(filtered)} persons → {out_path}")
    return filtered


if __name__ == "__main__":
    step_filter_people(OUTPUT_DIR)
