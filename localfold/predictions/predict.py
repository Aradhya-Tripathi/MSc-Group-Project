import os
from pathlib import Path


from colabfold.download import download_alphafold_params


class Model:
    @classmethod
    def setup(cls, is_complex: bool = False, model_type: str = "auto"):
        from colabfold.batch import set_model_type

        return set_model_type(is_complex, model_type)


class Input:
    @classmethod
    def setup(cls, path_to_input: str):
        from colabfold.batch import get_queries

        return get_queries(path_to_input)


class Predict:
    def __init__(
        self,
        path_to_input: str,
        path_to_params: str | Path,
        model_type: str = "auto",
        path_to_results_dir: str = ".",
    ) -> None:
        self.queries, self.is_complex = Input.setup(path_to_input=path_to_input)
        self.path_to_params = Path(path_to_params)
        self.path_to_results_dir = Path(path_to_results_dir)
        self.model_type = Model.setup(self.is_complex, model_type)

        if not self.check_existing_params():
            print(f"Could not find params at {self.path_to_params.absolute()}")

            exit()

        print(
            f"[READY TO PREDICT] using parameters: {self.path_to_params.absolute()} to predict: {path_to_input}"
        )

    def check_existing_params(self) -> bool:
        """
        Check if pre-trained model exists
        """
        if self.path_to_params:
            return os.path.exists(self.path_to_params.absolute())
        return False

    def run(self, **kwargs) -> dict[str, list]:
        from colabfold.batch import run

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
            user_agent="af-predictions/localfold",
            *kwargs,
        )
        return results

    def test_run(self):
        print("Run started!")
        import time

        time.sleep(10)
        return "Job Completed"


def cli():
    import sys

    if len(sys.argv) > 1:
        flag = sys.argv[1]
        match flag:
            case "--download-parameters":
                try:
                    data_dir = sys.argv[2]
                    model_type = sys.argv[3]
                except IndexError:
                    print(
                        "Please provide all the path to model parameters and the model type!"
                    )
                    sys.exit(-1)
                download_alphafold_params(
                    model_type=model_type, data_dir=Path(data_dir)
                )
            case "--predict":
                try:
                    path_to_input = sys.argv[2]
                    path_to_parameters = sys.argv[3]
                    path_to_results_dir = sys.argv[4]
                except IndexError:
                    print(
                        "Please provide all the path to model parameters, input and result dirs!"
                    )
                    sys.exit(-1)

                try:
                    model_type = sys.argv[5]
                except IndexError:
                    model_type = "auto"

                Predict(
                    path_to_input=path_to_input,
                    path_to_params=path_to_parameters,
                    path_to_results_dir=path_to_results_dir,
                    model_type=model_type,
                ).run()

    else:
        print(
            "Use the following for downloding the parameters: --download-parameters"
            "path/to/parameters and model-type or --predict flag"
        )


if __name__ == "__main__":
    cli()
