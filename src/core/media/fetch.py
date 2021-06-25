import cid, os
from .process import fetch_file


def _resources(resource, get_dir=lambda x: '', get_index=lambda x: 'index'):
    """
    Generic fetch process for resources
    :param resource:
    :param get_dir:
    :param get_index:
    :return:
    """

    if cid.is_cid(resource['route']):
        resource['abs'] = True
        return resource

    # If index defined keep using it else get index from param function
    resource_origin = resource['route']  # Input dir resource
    resource['index'] = resource.get('index', get_index(resource))
    resource_dir = get_dir(resource)  # Process dir from param function
    fetch_file(resource_origin, resource_dir)


def video_resources(mv, current_dir) -> dict:
    """
    Check if resources need to be downloaded and download it
    :param mv: MovieSchema dict
    :param current_dir: Storage dir
    :return: MovieSchema dict
    """

    def build_dir(r):  # process output dir
        return f"{current_dir}/{r.get('quality')}/{r.get('index')}"

    for resource in mv['resource']['videos']:
        _resources(resource, build_dir)
    return mv


def image_resources(mv, current_dir) -> dict:
    """
    Check if images need to be downloaded and download it
    :param mv: MovieSchema dict
    :param current_dir: Storage dir
    :return: MovieScheme dict
    """
    for _, resource in mv['resource']['posters'].items():
        _resources(
            resource,
            lambda r: f"{current_dir}/{r.get('index')}",
            lambda r: os.path.basename(r['route']),
        )
    return mv
