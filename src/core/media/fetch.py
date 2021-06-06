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
    resource['index'] = resource['index'] if 'index' in resource else get_index(resource)
    resource_origin = resource['route']  # Input dir resource
    resource_dir = get_dir(resource)  # Process dir from param function
    fetch_file(resource_origin, resource_dir)


def video_resources(mv, current_dir) -> dict:
    """
    Check if resources need to be downloaded and download it
    :param mv: MovieSchema dict
    :param current_dir: Storage dir
    :return: MovieSchema dict
    """

    for resource in mv['resource']['videos']:
        _resources(resource, lambda r: '%s/%s/%s' % (current_dir, r['quality'], r['index']))
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
            lambda r: '%s/%s' % (current_dir, r['index']),
            lambda r: os.path.basename(r['route']),
        )
    return mv
