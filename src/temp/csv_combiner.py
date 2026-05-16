import csv
import glob

files = glob.glob("results_*.csv")
combined_data = []
fieldnames = []

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        # Capture fieldnames from the first file
        if not fieldnames:
            fieldnames = reader.fieldnames
        for row in reader:
            combined_data.append(row)

# Write out the combined file
with open("final_report.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(combined_data)