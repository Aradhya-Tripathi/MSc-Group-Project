import os
from pathlib import Path

from colabfold.batch import run
from colabfold.download import download_alphafold_params

from model import Model
from model_input import Input


class Predict:
    def __init__(
        self,
        path_to_input: str,
        path_to_params: str | Path | None = None,
        model_type: str = "auto",
        path_to_results_dir: str = ".",
    ) -> None:
        self.queries, self.is_complex = Input.setup(path_to_input=path_to_input)
        self.path_to_params = Path(path_to_params)
        self.path_to_results_dir = Path(path_to_results_dir)
        self.model_type = Model.setup(self.is_complex, model_type)

        if not self.check_existing_params():
            print(f"Could not find params at {self.path_to_params.absolute()}")
            download = input("Do you want to download params? y/N: ")
            if download.casefold() == "y":
                download_alphafold_params(
                    model_type=self.model_type, data_dir=self.path_to_params
                )
            else:
                exit()

    def check_existing_params(self) -> bool:
        """
        Check if pre-trained model exists
        """
        if self.path_to_params:
            return os.path.exists(self.path_to_params.absolute())
        return False

    def run(self, **kwargs) -> dict[str, list]:
        print("Running model this might take some time")
        results = run(
            queries=self.queries,
            is_complex=self.is_complex,
            use_templates=kwargs.get("use_templates", False),
            custom_template_path=kwargs.get("custom_template_path", None),
            num_relax=kwargs.get("num_relax", 0),
            num_recycles=kwargs.get("num_recycles", 3),
            msa_mode=kwargs.get("msa_mode", "mmseqs2_uniref_env"),
            model_type=self.model_type,
            result_dir=self.path_to_results_dir,
            num_models=kwargs.get("num_models", 5),
            data_dir=self.path_to_params,
            *kwargs,
        )
        print("Finished runnign model")
        return results
