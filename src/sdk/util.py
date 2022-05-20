from src.core.scheme.definition.movies import MovieScheme

def build_dir(movie: MovieScheme):
    """Build current local dir path for movie

    :param: movie MovieSchema
    :return: resolved directory for movie
    :rtype: str
    """
    current_imdb_code = movie.imdb_code
    current_linked_name = getattr(movie, "group_name", None)
    current_dir = current_imdb_code
    if current_linked_name:  # If linked_name add sub-dir
        current_dir = f"{current_linked_name}/{current_imdb_code}"
    return current_dir
