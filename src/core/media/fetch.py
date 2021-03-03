import cid, os
from .download import download_file


def fetch_movie_resources(mv, current_imdb_code) -> dict:
    """
    Check if resources need to be downloaded and download it
    :param mv: MovieSchema dict
    :param current_imdb_code: Imdb code key in collection
    :return: MovieSchema dict
    """
    for resource in mv['resource']['videos']:
        if cid.is_cid(resource['route']):
            resource['abs'] = True
            continue

        resource['index'] = resource['index'] if 'index' in resource else 'index'
        resource_dir = '%s/%s/%s' % (current_imdb_code, resource['quality'], resource['index'])
        download_file(resource['route'], resource_dir)
    return mv


def fetch_images_resources(mv, current_imdb_code) -> dict:
    """
    Check if images need to be downloaded and download it
    :param mv: MovieSchema dict
    :param current_imdb_code: Imdb code key in collection
    :return: MovieScheme dict
    """

    for _, v in mv['resource']['images'].items():
        # Check for valid cid
        if cid.is_cid(v['route']):
            v['abs'] = True
            continue

        index = os.path.basename(v['route'])
        download_file(v['route'], "%s/%s" % (current_imdb_code, index))
        v['index'] = v['index'] if 'index' in v else index
    return mv
