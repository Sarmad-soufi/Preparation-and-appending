import re
import argparse

#parser = argparse.ArgumentParser(description="Insert AutoDock4 energies into column (put prefered column number).")
#parser.add_argument("file_name", help="Path to results.txt")
#parser.add_argument("file_name", help="path to input file")
#parser.add_argument("file_name", help="path to output")

args = parser.parse_args()

vinardo_txt = args.vinardo_txt
input_csv = args.input_csv
output_csv = args.output_csv

vinardo_dict = {}

with open(vinardo_txt, "r") as f:
    for line in f:
        match = re.search(r"(ZINC\d+_\d+).*?VINA RESULT:\s+(-?\d+\.\d+)", line)
        if match:
            zinc_id = match.group(1)
            energy = float(match.group(2))
            vinardo_dict[zinc_id] = energy

print(f"Parsed {len(vinardo_dict)} Vinardo energies.")

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

        while len(columns) < #: #adjust to the columm you want the data to be parsed into
            columns.append("")

        zinc_id = columns[0]
        energy = vinardo_dict.get(zinc_id, "")

        columns[#] = str(energy)

        outfile.write(",".join(columns) + "\n")

print("Finished. Vinardo energies inserted into column #.")
