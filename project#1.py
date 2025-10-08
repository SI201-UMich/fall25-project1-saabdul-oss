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


