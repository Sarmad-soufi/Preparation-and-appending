
from pathlib import Path
from rdkit import Chem
from rdkit.Chem import Crippen
from rdkit.Chem import rdFMCS
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "filename",
    help="Path to the input file"
)
parser.add_argument(
    "--sim",
    type=float,
    required=True,
    help="A number between 0.0 and 1.0"
)

args = parser.parse_args()

# load retro 2 structure
r2_smiles = "CC1=CC=C(S1)CNC1=CC=CC=C1C(=O)NC1CCCCC1"
r2 = Chem.MolFromSmiles(r2_smiles)

output_lines = []

with open(args.filename, "r") as smi_file:
    for line in smi_file:
        smi = line.split()[0]
        mol = Chem.MolFromSmiles(smi)
        if mol is None:
            continue

        logp = Crippen.MolLogP(mol)

        res = rdFMCS.FindMCS([r2, mol], completeRingsOnly=True)
        sim = res.numAtoms/r2.GetNumAtoms()
        if sim >= args.sim:
            print(f"{smi},{sim:.2f},{logp:.2f},{mol.GetNumAtoms()}")
            #print(res.numAtoms, mol.GetNumAtoms(), r2.GetNumAtoms())
            #print(Chem.MolToMolFile(Chem.MolFromSmarts(res.smartsString), "b.mol"))



