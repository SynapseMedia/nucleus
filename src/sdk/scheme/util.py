from src.sdk.media.storage.ipfs import dag_get
from .definition.movies import MultiMediaScheme
from src.sdk.constants import (
    DASH_NEW_FILENAME,
    HLS_NEW_FILENAME,
    HLS_FORMAT,
    DASH_FORMAT,
)


def fit_image_resource_from_dag(cid):
    """Process dag output standard scheme for image resource

    :param cid: IPFS cid
    :return: Dictionary with standard scheme for image resource
    """
    image = dag_get(f"{cid}/image")["Links"]
    image_resources = {i["Name"].split(".")[0]: f"/image/{i['Name']}" for i in image}
    return {
        "route": cid,
        "index": image_resources,
    }


def fit_video_resource_from_dag(cid):
    """Process dag output standard scheme for video resource

    :param cid: IPFS cid
    :return: Dictionary with standard scheme for video resource
    """
    protocol = {
        DASH_FORMAT: DASH_NEW_FILENAME,
        HLS_FORMAT: HLS_NEW_FILENAME,
    }

    video = dag_get(f"{cid}/movie")["Links"]
    # Mapping file => path from dag response
    video_resource = {
        i["Name"]: f"/movie/{i['Name']}/{protocol.get(i['Name'], HLS_NEW_FILENAME)}"
        for i in video
    }

    return {
        "route": cid,
        "index": video_resource,
    }


# TODO write tests
def fit_resources_from_dag(cid):
    """
    Process dag output to standard scheme definition to store in storage freeze
    :param cid: IPFS cid from where to get directories information
    :return: Dictionary with standard schema resources
    """
    video = fit_video_resource_from_dag(cid)
    image = fit_image_resource_from_dag(cid)
    return MultiMediaScheme().load({"video": video, "image": image})
