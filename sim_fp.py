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

drug_smiles = "input the reference drug smiles"
drug = Chem.MolFromSmiles(drug_smiles)

drug_fp = AllChem.GetMorganFingerprintAsBitVect(
    drug,
    radius=2,  #these settings are usually applied in literature for ideal morgan fingerprinting
    nBits=2048
)

with open(args.filename, "r") as smi_file:
    for line in smi_file:
        smi = line.split()[0]
        mol = Chem.MolFromSmiles(smi)

        if mol is None:
            continue

        logp = Crippen.MolLogP(mol)
        
        mol_fp = AllChem.GetMorganFingerprintAsBitVect(
            mol,
            radius=2,
            nBits=2048
        )

        sim = DataStructs.TanimotoSimilarity(drug_fp, mol_fp)

        if sim >= args.sim:
            print(f"{smi},{sim:.2f},{logp:.2f},{mol.GetNumAtoms()}")
