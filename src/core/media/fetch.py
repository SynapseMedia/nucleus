import cid, os
from .download import download_file


def fetch_movie_resources(mv, current_dir) -> dict:
    """
    Check if resources need to be downloaded and download it
    :param mv: MovieSchema dict
    :param current_dir: Imdb code key in collection
    :return: MovieSchema dict
    """
    for video in mv['resource']['videos']:
        if cid.is_cid(video['route']):
            video['abs'] = True
            continue

        video['index'] = video['index'] if 'index' in video else 'index'
        resource_dir = '%s/%s/%s' % (current_dir, video['quality'], video['index'])
        download_file(video['route'], resource_dir)
    return mv


def fetch_images_resources(mv, current_dir) -> dict:
    """
    Check if images need to be downloaded and download it
    :param mv: MovieSchema dict
    :param current_dir: Imdb code key in collection
    :return: MovieScheme dict
    """

    for _, image in mv['resource']['images'].items():
        # Check for valid cid
        if cid.is_cid(image['route']):
            image['abs'] = True
            continue

        image['index'] = image['index'] if 'index' in image else os.path.basename(image['route'])
        download_file(image['route'], "%s/%s" % (current_dir, image['index']))
    return mv
