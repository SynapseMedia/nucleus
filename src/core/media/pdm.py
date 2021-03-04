import csv
from .download import ROOT_PATH


def get_pb_domain_set(csv_file: str = 'pdm.csv') -> set:
    """
    Get public domain movies from csv
    :param csv_file: Path to csv file with pre-defined PDM movies list
    :return: Unique list of PDM
    """
    with open(f"{ROOT_PATH}/{csv_file}", 'r') as f:
        reader = csv.reader(f)
        return set([row[1] for row in reader])
