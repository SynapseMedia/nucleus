def clean_resource(resources):
    # Clean resource url if defined
    for resource in resources:
        if 'route' in resource:
            del resource['route']
    return resources


def clean_resources(mv: dict) -> dict:
    """
    Clean url key from schema
    :param mv: MovieSchema
    :return: Cleaned schema
    """

    # Clean resource route if defined
    clean_resource(mv['resource']['posters'].values())
    clean_resource(mv['resource']['videos'])
    return mv


def migrate_resource_hash(mv: dict, hash_: str) -> dict:
    """
    Re-struct resources adding the corresponding cid
    :param mv: MovieScheme dict
    :param hash_: CID hash
    :return: MovieScheme with CID assoc
    """
    for v in mv['resource']['videos']:
        v['cid'] = v.get('route') if 'abs' in v else hash_
    return mv


def migrate_image_hash(mv: dict, hash_: str) -> dict:
    """
    Re-struct image resources adding the corresponding cid
    :param mv: MovieScheme dict
    :param hash_: CID hash
    :return: MovieScheme with CID assoc
    """
    for _, v in mv['resource']['posters'].items():
        v['cid'] = v.get('route') if 'abs' in v else hash_
    return mv
