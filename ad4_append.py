import re
import argparse

#parser = argparse.ArgumentParser(description="Insert AutoDock4 energies into column (put prefered column number).")
#parser.add_argument("file_name", help="Path to results.txt")
#parser.add_argument("file_name", help="path to input file")
#parser.add_argument("file_name", help="path to output")

args = parser.parse_args()

ad4_dict = {}

with open(args.ad4_txt) as f:
    for line in f:
        match = re.search(r"(ZINC\d+_\d+)_out.*?VINA RESULT:\s*(-?\d+\.\d+)", line)
        if match:
            zinc_id = match.group(1)   # remove _out
            energy = float(match.group(2))
            ad4_dict[zinc_id] = energy

print(f"Parsed {len(ad4_dict)} AutoDock4 energies.")

with open(args.input_csv) as infile, open(args.output_csv, "w") as outfile:

    header = infile.readline().strip().split(",")

    while len(header) < 9:
        header.append("")

    header[8] = "AutoDock4_Energy"
    outfile.write(",".join(header) + "\n")

    for line in infile:
        line = line.strip()
        if not line:
            continue

        columns = line.split(",")

        while len(columns) < 9:
            columns.append("")

        zinc_id = columns[0]
        energy = ad4_dict.get(zinc_id, "")

        columns[8] = str(energy)

        outfile.write(",".join(columns) + "\n")

print("Finished. AutoDock4 energies inserted into column #.")
