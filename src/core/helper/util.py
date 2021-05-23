def build_dir(movie: dict):
    """
    Build current local dir for movie
    :param movie MovieSchema /scheme/definition.py
    :return:
    """
    current_imdb_code = movie.get('imdb_code')
    current_linked_name = movie.get('group_name', None)
    current_dir = current_imdb_code
    if current_linked_name:  # If linked_name add sub-dir
        current_dir = f"{current_linked_name}/{current_imdb_code}"
    return current_dir
