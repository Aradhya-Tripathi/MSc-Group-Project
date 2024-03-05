from colabfold.batch import get_queries


class Input:
    @classmethod
    def setup(cls, path_to_input: str):
        return get_queries(path_to_input)
