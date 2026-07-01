import re
import argparse

#parser = argparse.ArgumentParser(description="Insert AutoDock4 energies into column (put prefered column number).")
#parser.add_argument("file_name", help="Path to results.txt")
#parser.add_argument("file_name", help="path to input file")
#parser.add_argument("file_name", help="path to output")

args = parser.parse_args()

vina_txt = args.vina_txt
input_csv = args.input_csv
output_csv = args.output_csv

energy_dict = {}

with open(vina_txt, "r") as f:
    for line in f:
        match = re.search(r"(ZINC\d+_\d+).*?VINA RESULT:\s+(-?\d+\.\d+)", line)
        if match:
            zinc_id = match.group(1)
            energy = float(match.group(2))
            energy_dict[zinc_id] = energy

print(f"Parsed {len(energy_dict)} docking energies.")

with open(input_csv, "r") as infile, open(output_csv, "w") as outfile:

    header = infile.readline().strip().split(",")

    while len(header) < 7:
        header.append("")

    header[6] = "Vina_Energy"
    outfile.write(",".join(header) + "\n")

    for line in infile:
        line = line.strip()
        if not line:
            continue

        columns = line.split(",")

        while len(columns) < #:
            columns.append("")

        zinc_id = columns[0]
        energy = energy_dict.get(zinc_id, "")

        columns[6] = str(energy)
        outfile.write(",".join(columns) + "\n")

print("Finished. Energies inserted into column #.")

