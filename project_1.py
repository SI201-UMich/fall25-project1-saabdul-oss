# Name: Sarah Abdullah
# ID: 2419 6395
# email: saabdul@umich.edu
# Collaborators: Working alone but used ChatGPT
# Statement on AI:
import csv
import os
# Read CSV into a list of dictionaries
def load_csv(filename):
    rows = []
    source_dir = os.path.dirname(__file__)
    full_path = os.path.join(source_dir, filename)

    with open(full_path, newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        for raw in reader:
            row = clean_row(raw)
            rows.append(row)
    return rows

def clean_row(row):
    for k, v in row.items():
        if isinstance(v, str):
            row[k] = v.strip()
    def to_float(x):
        try:
            return float(x)
        except:
            return None
    def to_int(x):
        try:
            return int(float(x))
        except:
            return None
        
    row["bill_length_mm"] = to_float(row.get("bill_length_mm"))
    row["bill_depth_mm"] = to_float(row.get("bill_depth_mm"))
    row["flipper_length_mm"] = to_float(row.get("flipper_length_mm"))
    row["body_mass_g"] = to_float(row.get("body_mass_g"))
    row["year"] = to_int(row.get("year"))

    return row

# Calculation 1 (Average) Mean flipper length by (species, island) for a chosen year
def calc_avg_flipper_by_species_island(rows, year):
    groups = {}
    for r in rows:
        if r.get("year") != year:
            continue
        species = r.get("species")
        island = r.get("island")
        flipper_len = r.get("flipper_length_mm")

        if not species or not island:
            continue
        if flipper_len is None:
            continue

        key = (species, island)
        if key not in groups:
            groups[key] = {"sum": 0.0, "count": 0}
        groups[key]["sum"] += flipper_len
        groups[key]["count"] += 1
    # Build output rows with averages
    table = []
    for (species, island), group_stats in groups.items():
        if group_stats["count"] == 0:
            continue
        mean_flipper = group_stats["sum"] / group_stats["count"]
        table.append({"species": species, "island": island, "year": year, "mean_flipper_mm": mean_flipper, "N": group_stats["count"]})

# Calculation 2 (Percentage) % of large penguins by sex
def calc_pct_large_by_sex(rows):
    counts = {}
    for r in rows:
        sex = r.get("sex")
        mass = r.get("body_mass_g")
        bill_len = r.get("bill_length_mm")

        if not sex or mass is None or bill_len is None:
            continue
        if sex not in counts:
            counts[sex] = {"total": 0, "large": 0}
        counts[sex]["total"] += 1
        if mass >= 40000.0 and bill_len >= 45.0:
            counts[sex]["large"] += 1
    # Build output rows with percentages
    table = []
    for sex, c in counts.items():
        total = c["total"]
        large = c["large"]
        if total == 0:
            continue
        pct_large = 100 * large / total
        table.append({"sex": sex, "pct_large": pct_large, "N": total})
    table.sort(key=lambda d: d["sex"])
    return table







# Print column names, total row count and the first n rows 
def preview_data(rows, n=5):
    if not rows:
        print("No data loaded.")
        return
    print("Columns:", list(rows[0].keys()))
    print("Total rows:", len(rows))
    print("Sample rows:")
    for r in rows[:n]:
        print(r)

def main():
    filename = "penguins.csv"
    rows = load_csv(filename)
    preview_data(rows, n=5)

if __name__ == "__main__":
    main()

import unittest
from project_1 import (calc_avg_flipper_by_species_island, calc_pct_big_by_sex)

def row(species=None, island=None, flipper=None, year=None, sex=None, mass=None, bill_len=None):
    return {"species": species, "island": island, "flipper_length_mm": flipper, "year": year, "sex": sex, "body_mass_g": mass, "bill_length_mm": bill_len}

class TestCalcAvgFlipperBySpeciesIsland(unittest.TestCase):
    def test_basic_two_species_two_islands_single_year(self):
        rows = [row("Adelie", "Torgersen", 180.0, 2007), row("Adelie", "Torgersen", 190.0, 2007), row("Gentoo", "Biscoe", 200.0, 2007), row("Gentoo", "Biscoe", 220.0, 2007), row("Adelie", "Torgersen", 999.0, 2008)]
        out = calc_avg_flipper_by_species_island(rows, 2007)
        m = {(d["species"], d["island"]): d for d in out}
        self.assertIn(("Adelie","Torgersen"), m)
        self.assertIn(("Gentoo","Biscoe"), m)
        self.assertEqual(m[("Adelie","Torgersen")]["N"], 2)
        self.assertAlmostEqual(m[("Adelie","Torgersen")]["mean_flipper_mm"], (180+190)/2, places=6)
        self.assertEqual(m[("Gentoo","Biscoe")]["N"], 2)
        self.assertAlmostEqual(m[("Gentoo","Biscoe")]["mean_flipper_mm"], (200+220)/2, places=6)

    def test_filter_by_year_changes_groups(self):
        rows = [row("Adelie", "Dream", 185.0, 2008), row("Adelie", "Dream", 195.0, 2008), row("Adelie", "Dream", 175.0, 2007)]
        out_2008 = calc_avg_flipper_by_species_island(rows, 2008)
        m = {(d["species"], d["island"]): d for d in out_2008}
        self.assertEqual(set(m.keys()), {("Adelie","Dream")})
        self.assertEqual(m[("Adelie","Dream")]["N"], 2)
        self.assertAlmostEqual(m[("Adelie","Dream")]["mean_flipper_mm"], (185+195)/2, places=6)   
    # Edge cases
    def test_missing_flipper_values_are_ignored(self):
        rows = [row("Adelie", "Torgersen", None, 2007), row("Adelie", "Torgersen", "", 2007), row("Adelie", "Torgersen", 200.0, 2007)]
        out = calc_avg_flipper_by_species_island(rows, 2007)
        self.assertEqual(len(out), 1)
        d = out[0]
        self.assertEqual(d["species"], "Adelie")
        self.assertEqual(d["island"], "Torgersen")
        self.assertEqual(d["N"], 1)
        self.assertAlmostEqual(d["mean_flipper_mm"], 200.0, places=6)

    def test_no_rows_for_year_returns_empty_list(self):
        rows = [row("Adelie", "Torgersen", 180.0, 2007), row("Gentoo", "Biscoe", 200.0, 2007)]
        out = calc_avg_flipper_by_species_island(rows, 1999)
        self.assertEqual(out, []) 

class TestCalcPctBigBySex(unittest.TestCase):
    def test_pct_big_both_sexes_mixed(self):
        rows = [row(sex="female", mass=4100.0, bill_len=46.0), row(sex="female", mass=3950.0, bill_len=46.0), row(sex="female", mass=4100.0, bill_len=44.0), row(sex="male", mass=4050.0, bill_len=47.0), row(sex="male", mass=4200.0, bill_len=45.0), row(sex="male", mass=3000.0, bill_len=46.0)]
        out = calc_pct_big_by_sex(rows)
        m = {d["sex"]: d for d in out}
        self.assertIn("female", m)
        self.assertIn("male", m)
        self.assertEqual(m["female"]["N"], 3)
        self.assertEqual(m["male"]["N"], 3)
        self.assertAlmostEqual(m["female"]["pct_big"], 100.0*(1/3), places=2)
        self.assertAlmostEqual(m["male"]["pct_big"],   100.0*(2/3), places=2)

    def test_threshold_inclusive(self):
        rows = [row(sex="male", mass=4000.0, bill_len=45.0), row(sex="male", mass=3999.9, bill_len=45.0), row(sex="female", mass=4100.0, bill_len=44.9), row(sex="female", mass=4100.0, bill_len=45.0)]
        out = calc_pct_big_by_sex(rows)
        m = {d["sex"]: d for d in out}
        self.assertAlmostEqual(m["male"]["pct_big"], 50.0, places=6)
        self.assertAlmostEqual(m["female"]["pct_big"], 50.0, places=6)
    # Edge Cases
    def test_missing_sex_rows_are_excluded(self):
        rows = [row(sex=None, mass=5000.0, bill_len=50.0), row(sex="", mass=5000.0, bill_len=50.0), row(sex="male", mass=4000.0, bill_len=45.0)]
        out = calc_pct_big_by_sex(rows)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["sex"], "male")
        self.assertEqual(out[0]["N"], 1)
        self.assertAlmostEqual(out[0]["pct_big"], 100.0, places=6)

    def test_sex_with_no_usable_rows_is_skipped(self):
        rows = [row(sex="female", mass=4100.0, bill_len=46.0), row(sex="female", mass=3000.0, bill_len=46.0)]
        out = calc_pct_big_by_sex(rows)
        m = {d["sex"]: d for d in out}
        self.assertIn("female", m)
        self.assertNotIn("male", m)
        self.assertEqual(m["female"]["N"], 2)

