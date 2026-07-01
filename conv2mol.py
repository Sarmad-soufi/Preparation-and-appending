import argparse
from pathlib import Path
from rdkit import Chem
from rdkit.Chem import Crippen, rdFMCS, AllChem
from rdkit.Chem import rdmolfiles

# -------------------------
# Command-line arguments
# -------------------------
parser = argparse.ArgumentParser()
parser.add_argument("filename", help="Path to the input SMILES file")
parser.add_argument("--sim", type=float, required=True,
                    help="Similarity threshold (0.0–1.0)")
args = parser.parse_args()

SCRIPT_DIR = Path(__file__).resolve().parent

# -------------------------
# Load (retro 2)
# -------------------------
r2_smiles = "CC1=CC=C(S1)CNC1=CC=CC=C1C(=O)NC1CCCCC1"
r2 = Chem.MolFromSmiles(r2_smiles)

# -------------------------
# Process each SMILES in the input file
# -------------------------
with open(args.filename, "r") as smi_file:
    for idx, line in enumerate(smi_file, 1):
        smi = line.split()[0]
        mol = Chem.MolFromSmiles(smi)

        if mol is None:
            print(f"Line {idx}: invalid SMILES")
            continue

        # Calculate logP
        logp = Crippen.MolLogP(mol)

        # Compute FMC similarity
        res = rdFMCS.FindMCS([r2, mol], completeRingsOnly=True)
        sim = res.numAtoms / r2.GetNumAtoms()

        # Only process molecules above similarity threshold
        if sim >= args.sim:
            # Add hydrogens and generate 3D coordinates
            mol3d = Chem.AddHs(mol)
            ret = AllChem.EmbedMolecule(mol3d, randomSeed=42)
            if ret != 0:
                print(f"Line {idx}: embedding failed")
                continue

            AllChem.UFFOptimizeMolecule(mol3d)

            # Save as MOL file (3D coordinates included)
            out_file = SCRIPT_DIR / f"compound_{idx}_sim_{sim:.2f}.mol"
            rdmolfiles.MolToMolFile(mol3d, str(out_file))

            print(f"Saved {out_file.name} | logP: {logp:.2f} | similarity: {sim:.2f}")
