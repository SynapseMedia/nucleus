from src.sdk import media, logger, util
from src.sdk.scheme.definition.movies import MovieScheme


def boot(current_movie: MovieScheme):
    """
    Boot static processing from metadata definition scheme
    :param current_movie: MovieScheme
    """
    # Process each video described in movie
    output_dir = util.build_dir(current_movie)
    logger.log.warn(f"Fetching posters for {current_movie.title}")
    media.static.ingest.images(
        image_path=current_movie.resource.image.route,  # input image path
        output_dir=output_dir,  # where store new images?
    )
