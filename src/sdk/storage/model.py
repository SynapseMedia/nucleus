from src.sdk.harvest.model import Media
from src.sdk.harvest.fields import FilePath, CIDString


class Stored(Media):
    route: CIDString


class File(Media):
    route: FilePath

    # TODO check que el input no sea igual que el PROD out path
    # TODO validate if is PROD path? o crear un ProdPath type :)
