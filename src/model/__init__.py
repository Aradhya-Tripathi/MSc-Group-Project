from colabfold.batch import set_model_type


class Model:
    @classmethod
    def setup(cls, is_complex: bool = False, model_type: str = "auto"):
        return set_model_type(is_complex, model_type)
