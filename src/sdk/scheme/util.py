from src.sdk.media.storage.ipfs import dag_get
from .definition.movies import MultiMediaScheme


# TODO write tests
def fit_resources_from_dag(cid):
    """
    Process dag output to standard scheme definition to store in storage freeze
    :param cid: From where to get directories information
    :return dict
    """
    video = dag_get(f"{cid}/movie")["Links"]
    image = dag_get(f"{cid}/images")["Links"]

    video_scheme = {
        "route": cid,
        "index": {i["Name"]: f"/movie/{i['Name']}/" for i in video},
    }
    image_scheme = {
        "route": cid,
        "index": {i["Name"].split(".")[0]: f"/images/{i['Name']}" for i in image},
    }

    return MultiMediaScheme().load({"video": video_scheme, "image": image_scheme})
