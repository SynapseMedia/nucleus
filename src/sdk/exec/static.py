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
    image_route = current_movie.resource.image.route

    # TODO validate standard ratio for image (500, 750)
    media.static.ingest.images(
        image_path=image_route,  # input image path
        output_dir=output_dir,  # where store new images?
    )
