import argparse
from pathlib import Path
from rdkit import Chem
from rdkit.Chem import Crippen, rdFMCS, AllChem
from rdkit.Chem import rdmolfiles

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="Path to the input SMILES file")
parser.add_argument("--sim", type=float, required=True,
                    help="Similarity threshold (0.0–1.0)")
args = parser.parse_args()

SCRIPT_DIR = Path(__file__).resolve().parent


#reference_smiles = "input smiles here"
#drug = Chem.MolFromSmiles(drug_smiles)

with open(args.filename, "r") as smi_file:
    for idx, line in enumerate(smi_file, 1):
        smi = line.split()[0]
        mol = Chem.MolFromSmiles(smi)

        if mol is None:
            print(f"Line {idx}: invalid SMILES")
            continue
          
        logp = Crippen.MolLogP(mol)

        res = rdFMCS.FindMCS([drug, mol], completeRingsOnly=True)
        sim = res.numAtoms / r2.GetNumAtoms()

        if sim >= args.sim:
            
            mol3d = Chem.AddHs(mol)
            ret = AllChem.EmbedMolecule(mol3d, randomSeed=42)
            if ret != 0:
                print(f"Line {idx}: embedding failed")
                continue

            AllChem.UFFOptimizeMolecule(mol3d)

            out_file = SCRIPT_DIR / f"compound_{idx}_sim_{sim:.2f}.mol"
            rdmolfiles.MolToMolFile(mol3d, str(out_file))

            print(f"Saved {out_file.name} | logP: {logp:.2f} | similarity: {sim:.2f}")
