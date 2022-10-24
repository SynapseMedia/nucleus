import fnmatch, os
from src.sdk import cache
from src.sdk.constants import WALLET_PUBLIC_KEY


class PDM:

    def __str__(self) -> str:
        return 'pdm'

    @classmethod
    def fetch_quality_file(cls, movie_path, quality):
        for root, dirnames, filenames in os.walk(movie_path):
            if quality in root:
                for filename in fnmatch.filter(filenames, '*.mp4'):
                    return f"{root}/{filename}"

    def __call__(self, scheme):
        pdm_db, = cache.get_dbs('witthi')
        result, _ = cache.manager.retrieve(pdm_db, {'group_name': 'pdm'})
        root_path = '/multimedia/raw/pdm'

        for movie in result:
            del movie['_id']
            movie['creator'] = WALLET_PUBLIC_KEY
            imdb_code = movie.get('imdb_code')
            movie_path = f"{root_path}/{imdb_code}/"
            movie_posters = movie.get('resource').get('image')
            path_720 = self.fetch_quality_file(movie_path, '720p')
            path_1080 = self.fetch_quality_file(movie_path, '1080p')

            if not path_1080 and not path_720:
                continue

            yield [{
                **movie,
                **{
                    'resource': {
                        'video': {'route': path_1080 if path_1080 else path_720},
                        'image': movie_posters
                    }
                }
            }]
