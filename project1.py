# Name: Sarah Abdullah
# ID: 24196395
# email: saabdul@umich.edu
# Collaborators: Working alone but used Chat GPT
# Statement on AI: 

import csv
import os
# Read a CSV file into a list of dictionaries where each row is a dictionary and the keys are column headers
def load_csv(filename):
    rows = []
    source_dir = os.path.dirname(__file__)
    full_path = os.path.join(source_dir, filename)
    with open(full_path, newline='', encoding='utf-8') as infile:
        csv_reader = csv.DictReader(infile)
        for row in csv_reader:
            rows.append(row)
    return rows
# Print column names, total row count, and the first n rows
def preview_data(rows, n=5):
    if not rows:
        print("No data loaded.")
        return
    print("Columns:", list(rows[0].keys()))
    print("Total rows:", len(rows))
    print("Sample rows:")
    for row in rows[:n]:
        print(row)
def main():
    filename = "Electric_Vehicle_Population_Data (1).csv"
    data = load_csv(filename)
    preview_data(data, n=5)
if __name__ == "__main__":
    main()