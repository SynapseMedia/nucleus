from .definition.movies import MultiMediaScheme
from src.core.storage.ipfs import dag_get
from src.core.constants import (
    DASH_NEW_FILENAME,
    HLS_NEW_FILENAME,
    HLS_FORMAT,
    DASH_FORMAT,
)


def fit_image_from_dag(cid: str):
    """Process dag output standard scheme for image resource

    :param cid: IPFS cid
    :return: Dictionary with standard scheme for image resource
    :rtype: dict
    """
    image = dag_get(f"{cid}/image")["Links"]
    image_resources = {i["Name"].split(".")[0]: f"/image/{i['Name']}" for i in image}
    return {
        "route": cid,
        "index": image_resources,
    }


def fit_video_from_dag(cid: str):
    """Process dag output standard scheme for video resource

    :param cid: IPFS cid
    :return: Dictionary with standard scheme for video resource
    :rtype: dict
    """
    protocol = {
        DASH_FORMAT: DASH_NEW_FILENAME,
        HLS_FORMAT: HLS_NEW_FILENAME,
    }

    template_path = "/movie/%s/%s"
    video = dag_get(f"{cid}/movie")["Links"]
    build_path = lambda v: template_path % (v['Name'], protocol.get(v['Name']))
    # Mapping file => path from dag response
    video_resource = {i["Name"]: build_path(i) for i in video}

    return {
        "route": cid,
        "index": video_resource,
    }


def multimedia_resources_from_dag(cid: str):
    """Process dag output to standard resource scheme definition

    :param cid: IPFS cid
    :return: Dictionary with standard schema resources
    :rtype: MultiMediaScheme
    """
    video = fit_video_from_dag(cid)
    image = fit_image_from_dag(cid)
    return MultiMediaScheme().load({"video": video, "image": image})
