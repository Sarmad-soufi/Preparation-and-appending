import argparse
import time
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Extract PLP scores and append to CSV.")
    parser.add_argument("plp_dir", help="Path to the PLP out_per_ligand directory")
    parser.add_argument("input_csv", help="CSV already containing other energies")
    parser.add_argument("output_csv", help="Output CSV with PLP scores added")
    args = parser.parse_args()

    plp_dir = Path(args.plp_dir).resolve()
    plp_dict = {}

    t0 = time.time()
    print(f"\n[1/4] Script started. Target directory: {plp_dir}", flush=True)

    # 1. Map the directory
    print(f"[2/4] Mapping all bestranking.lst files... (If it freezes here, it's a hard drive / directory issue)", flush=True)
    lst_files = list(plp_dir.rglob("bestranking.lst"))
    
    t1 = time.time()
    print(f"      -> Success: Found {len(lst_files)} files in {t1 - t0:.2f} seconds.", flush=True)

    # 2. Extract Scores (Since the layout is identical to GOLD, we use columns[0])
    print("[3/4] Opening files and extracting PLP scores...", flush=True)
    for lst_file in lst_files:
        zinc_id = lst_file.parent.name 
        
        with open(lst_file, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                
                columns = line.split()
                if columns:
                    plp_dict[zinc_id] = columns[0]
                    break 

    t2 = time.time()
    print(f"      -> Success: Parsed {len(plp_dict)} scores in {t2 - t1:.2f} seconds.", flush=True)

    # 3. Write to CSV
    print(f"[4/4] Writing results to Column 13 in {args.output_csv}...", flush=True)
    with open(args.input_csv, "r") as infile, open(args.output_csv, "w") as outfile:
        header = infile.readline().strip().split(",")
        
        # Pad to 13 slots
        while len(header) < 13:
            header.append("")
        header[12] = "PLP_Score"
        outfile.write(",".join(header) + "\n")

        rows_processed = 0
        for line in infile:
            line = line.strip()
            if not line:
                continue

            columns = line.split(",")
            
            while len(columns) < 13:
                columns.append("")

            zinc_id = columns[0]
            score = plp_dict.get(zinc_id, "")

            columns[12] = str(score)

            outfile.write(",".join(columns) + "\n")
            rows_processed += 1

    t3 = time.time()
    print(f"      -> Success: Processed {rows_processed} CSV rows in {t3 - t2:.2f} seconds.", flush=True)
    print(f"\n✅ All done! Total execution time: {t3 - t0:.2f} seconds.\n", flush=True)

if __name__ == "__main__":
    main()
