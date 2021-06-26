import os
import src.core.helper as helper
from .process import fetch_file


def image_resources(mv, current_dir):
    """
    Check if images need to be downloaded and download it
    :param mv: MovieSchema dict
    :param current_dir: Storage dir
    :return: MovieScheme dict
    """

    for key, resource in mv['resource']['posters'].items():
        # If index defined keep using it else get index from param function
        file_name = os.path.basename(resource['route'])
        file_format = helper.util.extract_extension(file_name)
        resource_origin = resource['route']  # Input dir resource
        resource_dir = f"{current_dir}/{key}.{file_format}"  # Process dir from param function
        fetch_file(resource_origin, resource_dir)
