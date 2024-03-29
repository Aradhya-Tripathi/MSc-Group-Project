import requests


def uniprot(query_string: str):
    url = "https://rest.uniprot.org/uniprotkb/search"
    response = requests.get(
        url,
        params={
            "query": query_string,
            "format": "json",
            "includeIsoform": True,
        },
    )
    if response.ok:
        return response.json()
    return {}


def ready_to_go_alphafold(uniprot_accession: str):
    response = requests.get(
        f"https://alphafold.ebi.ac.uk/api/prediction/{uniprot_accession}"
    )
    if response.ok:
        return response.json()

    return {}


if __name__ == "__main__":
    query = "9606"
    ready_to_go = "P00520"
