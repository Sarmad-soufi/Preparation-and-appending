import re
import argparse

#parser = argparse.ArgumentParser(description="Insert AutoDock4 energies into column (put prefered column number).")
#parser.add_argument("file_name", help="Path to results.txt")
#parser.add_argument("file_name", help="path to input file")
#parser.add_argument("file_name", help="path to output")

args = parser.parse_args()

gpu_dict = {}

with open(args.gpu_txt) as f:
    for line in f:
        match = re.search(
            r"(ZINC\d+_\d+)\.pdbqt\s+Estimated Free Energy:\s*(-?\d+\.\d+)",
            line
        )
        if match:
            zinc_id = match.group(1)
            energy = float(match.group(2))
            gpu_dict[zinc_id] = energy

print(f"Parsed {len(gpu_dict)} GPU energies.")

with open(args.input_csv) as infile, open(args.output_csv, "w") as outfile:

    header = infile.readline().strip().split(",")

    while len(header) < 10:
        header.append("")

    header[9] = "AutoDockGPU_Energy"
    outfile.write(",".join(header) + "\n")

    for line in infile:
        line = line.strip()
        if not line:
            continue

        columns = line.split(",")

        while len(columns) < 10:
            columns.append("")

        zinc_id = columns[0]
        energy = gpu_dict.get(zinc_id, "")

        columns[9] = str(energy)

        outfile.write(",".join(columns) + "\n")

print("Finished. GPU energies inserted into column #.")
