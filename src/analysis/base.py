import os
import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)
from Bio import BiopythonDeprecationWarning
from Bio.PDB import PDBParser
from Bio.PDB.Structure import Structure

warnings.simplefilter(action="ignore", category=BiopythonDeprecationWarning)
import os
from pathlib import Path


class Analyse:
    def __init__(self, path_to_results: str | Path) -> None:
        self.path_to_results = Path(path_to_results).absolute()
        self.pdb_files: dict[str:Structure] = {}
        self.parser = PDBParser()

    def get_plot_files(self):
        for idx, entry in enumerate(os.scandir(self.path_to_results), start=1):
            if entry.name.endswith(".pdb"):
                full_path = os.path.join(self.path_to_results, entry.name)
                self.pdb_files[full_path] = self.parser.get_structure(idx, full_path)

        if not self.pdb_files:
            print("No plots found check results dir!")

        for file_name, structure in self.pdb_files.items():
            relative_name = file_name.split("/")[-1]
            print(f"\n\n---------------{relative_name}---------------\n\n")
            for model in structure:
                for chain in model:
                    for residue in chain:
                        for atom in residue:
                            print(atom, atom.get_vector())

    def coordinate_dump(self) -> None: ...


if __name__ == "__main__":
    Analyse("./results").get_plot_files()
