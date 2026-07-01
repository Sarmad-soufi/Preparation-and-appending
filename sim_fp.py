from pathlib import Path
from rdkit import Chem
from rdkit.Chem import Crippen
from rdkit.Chem import AllChem
from rdkit.CHem import DataStructs
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

# generate fingerprint for reference molecule
r2_fp = AllChem.GetMorganFingerprintAsBitVect(
    r2,
    radius=2,
    nBits=2048
)

with open(args.filename, "r") as smi_file:
    for line in smi_file:
        smi = line.split()[0]
        mol = Chem.MolFromSmiles(smi)

        if mol is None:
            continue

        logp = Crippen.MolLogP(mol)

        # generate fingerprint for query molecule
        mol_fp = AllChem.GetMorganFingerprintAsBitVect(
            mol,
            radius=2,
            nBits=2048
        )

        # calculate Tanimoto similarity
        sim = DataStructs.TanimotoSimilarity(r2_fp, mol_fp)

        if sim >= args.sim:
            print(f"{smi},{sim:.2f},{logp:.2f},{mol.GetNumAtoms()}")
