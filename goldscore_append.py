import argparse
from pathlib import Path

def main():
    #parser = argparse.ArgumentParser(description="Insert AutoDock4 energies into column (put prefered column number).")
    #parser.add_argument("file_name", help="Path to results.txt")
    #parser.add_argument("file_name", help="path to input file")
    #parser.add_argument("file_name", help="path to output")

    args = parser.parse_args()

    gold_dir = Path(args.gold_dir).resolve()
    gold_dict = {}

    lst_files = list(gold_dir.rglob("bestranking.lst"))
    
    for lst_file in lst_files:
        zinc_id = lst_file.parent.name 
        
        with open(lst_file, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                    
                columns = line.split()
                if columns:
                    fitness = columns[0]
                    gold_dict[zinc_id] = fitness
                    break

    print(f"Parsed {len(gold_dict)} GOLD fitness scores.")

    with open(args.input_csv, "r") as infile, open(args.output_csv, "w") as outfile
        header = infile.readline().strip().split(",")
        
        while len(header) < 11:
            header.append("")
        header[10] = "GOLD_Fitness"
        outfile.write(",".join(header) + "\n")

        for line in infile:
            line = line.strip()
            if not line:
                continue

            columns = line.split(",")
            
            while len(columns) < 11:
                columns.append("")

            zinc_id = columns[0]
            
            fitness = gold_dict.get(zinc_id, "")

            columns[10] = str(fitness)

            outfile.write(",".join(columns) + "\n")

    print("Finished. GOLD fitness scores inserted into column #.")

if __name__ == "__main__":
    main()
