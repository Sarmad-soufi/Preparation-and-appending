import re
import argparse

parser = argparse.ArgumentParser(description="Insert Vinardo energies into column 8.")
parser.add_argument("vinardo_txt", help="Path to vinardo_results.txt")
parser.add_argument("input_csv", help="CSV already containing Vina energies")
parser.add_argument("output_csv", help="Output CSV with Vinardo energies added")

args = parser.parse_args()

vinardo_txt = args.vinardo_txt
input_csv = args.input_csv
output_csv = args.output_csv

vinardo_dict = {}

# ---- Parse Vinardo results ----
with open(vinardo_txt, "r") as f:
    for line in f:
        match = re.search(r"(ZINC\d+_\d+).*?VINA RESULT:\s+(-?\d+\.\d+)", line)
        if match:
            zinc_id = match.group(1)
            energy = float(match.group(2))
            vinardo_dict[zinc_id] = energy

print(f"Parsed {len(vinardo_dict)} Vinardo energies.")

# ---- Insert into CSV ----
with open(input_csv, "r") as infile, open(output_csv, "w") as outfile:

    header = infile.readline().strip().split(",")

    while len(header) < 8:
        header.append("")

    header[7] = "Vinardo_Energy"
    outfile.write(",".join(header) + "\n")

    for line in infile:
        line = line.strip()
        if not line:
            continue

        columns = line.split(",")

        while len(columns) < 8:
            columns.append("")

        zinc_id = columns[0]
        energy = vinardo_dict.get(zinc_id, "")

        columns[7] = str(energy)

        outfile.write(",".join(columns) + "\n")

print("Finished. Vinardo energies inserted into column 8.")
