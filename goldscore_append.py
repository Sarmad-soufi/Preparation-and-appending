import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Extract GOLD fitness scores and append to CSV.")
    parser.add_argument("gold_dir", help="Path to the GOLD out_per_ligand directory")
    parser.add_argument("input_csv", help="CSV already containing other energies")
    parser.add_argument("output_csv", help="Output CSV with GOLD scores added")

    args = parser.parse_args()

    gold_dir = Path(args.gold_dir).resolve()
    gold_dict = {}

    # 1. Parse all bestranking.lst files
    # rglob will recursively find all files named bestranking.lst in the subfolders
    lst_files = list(gold_dir.rglob("bestranking.lst"))
    
    for lst_file in lst_files:
        # The parent folder name is the ZINC ID (e.g., ZINC001828406624_1)
        zinc_id = lst_file.parent.name 
        
        with open(lst_file, "r") as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comment lines
                if not line or line.startswith("#"):
                    continue
                
                # The first non-comment line contains the top-ranked score
                # split() without arguments breaks the line by any whitespace
                columns = line.split()
                if columns:
                    fitness = columns[0]
                    gold_dict[zinc_id] = fitness
                    break  # We only need the top-ranked score, so stop reading this file

    print(f"Parsed {len(gold_dict)} GOLD fitness scores.")

    # 2. Append to the CSV
    with open(args.input_csv, "r") as infile, open(args.output_csv, "w") as outfile:
        # Handle the header
        header = infile.readline().strip().split(",")
        
        # Ensure header is long enough, then set index 10 (11th column) for GOLD
        while len(header) < 11:
            header.append("")
        header[10] = "GOLD_Fitness"
        outfile.write(",".join(header) + "\n")

        # Handle the rows
        for line in infile:
            line = line.strip()
            if not line:
                continue

            columns = line.split(",")
            
            # Ensure the row has enough columns
            while len(columns) < 11:
                columns.append("")

            zinc_id = columns[0]
            # Get the fitness score, default to empty string if not found
            fitness = gold_dict.get(zinc_id, "")

            columns[10] = str(fitness)

            outfile.write(",".join(columns) + "\n")

    print("Finished. GOLD fitness scores inserted into column 11.")

if __name__ == "__main__":
    main()
