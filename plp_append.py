import argparse
import time
from pathlib import Path

def main():
    #parser = argparse.ArgumentParser(description="Insert AutoDock4 energies into column (put prefered column number).")
    #parser.add_argument("file_name", help="Path to results.txt")
    #parser.add_argument("file_name", help="path to input file")
    #parser.add_argument("file_name", help="path to output")

    plp_dir = Path(args.plp_dir).resolve()
    plp_dict = {}

    t0 = time.time()
    print(f"\n[1/4] Script started. Target directory: {plp_dir}", flush=True)

    print(f"[2/4] Mapping all bestranking.lst files... (If it freezes here, it's a hard drive / directory issue)", flush=True)
    lst_files = list(plp_dir.rglob("bestranking.lst"))
    
    t1 = time.time()
    print(f"      -> Success: Found {len(lst_files)} files in {t1 - t0:.2f} seconds.", flush=True)

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
    print(f"[4/4] Writing results to Column # in {args.output_csv}...", flush=True)
    with open(args.input_csv, "r") as infile, open(args.output_csv, "w") as outfile:
        header = infile.readline().strip().split(",")
        
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
