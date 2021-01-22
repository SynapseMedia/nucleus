import requests
from contextlib import contextmanager
from multiprocessing import Pool

from src.py import Log, logger
from src.py.media.ingest import get_pb_domain_set

__author__ = 'gmena'
POOL_PROCESS = 5
ROOT_API = 'https://yts.mx'


class YTS(object):
    """
    This class defines the basic interface called by the migrate process.

    These methods will be called by the migrate:
      request(query_string)
      get_movies(page)
      request_generator()

    In migrate process each page is requested to get JSON content, pre process it and return it
    To know more about YTS API doc https://yts.mx/api
    """

    def __str__(self):
        return 'YTS'

    def __init__(self, host: str = ROOT_API, page: int = 0, limit: int = 50):
        # ignore 400 cause by IndexAlreadyExistsException when creating an index

        # CONSTANTS
        self.YTS_HOST = '%s/api/v2/list_movies.json' % host
        self.YTS_RECURSIVE_LIMIT = limit  # limit result per page (step)

        self.yts_recursive_page = page  # start page
        self.yts_movies_indexed = dict()  # indexed
        self.req_session = requests.Session()
        self.pb_match = get_pb_domain_set()

    @contextmanager
    def request(self, query_string=None):
        """
        Handle http request
        :param query_string:
        :return:
        """
        # Request yifi
        _request: str = f"{self.YTS_HOST}{'?%s' % query_string if query_string else ''}"
        _cookie = 'adcashufpv3=17981512371092097718392042062; __cfduid=dbf1c05bdb221675033d2ae958eb4f2961610924444; PHPSESSID=vaddrbb83hnm7sfj1tgqc52shg; __atuvc=6%7C3'
        _agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'

        try:
            conn = self.req_session.get(
                url=_request,
                timeout=60,
                headers={
                    "content-type": "json",
                    'user-agent': _agent,
                    'cookie': _cookie
                }
            )

            # Return json
            yield conn.json()
        except (Exception,) as e:
            logger.error(f"{Log.FAIL}Fail request: {e}{Log.ENDC}")
            logger.warning(f"{Log.WARNING}Retrying..{Log.ENDC}")
            yield self.request(query_string)

    def get_movies(self, page):
        """
        Process request for movies from YTS
        :param page:
        :return:
        """
        # Req YTS
        logger.info(f"Requesting page {str(page)}")
        _uri = 'page=' + str(page) + '&limit=' + str(self.YTS_RECURSIVE_LIMIT) + '&sort=date_added'
        with self.request(_uri) as conn_result:
            if not 'data' in conn_result:
                logger.debug(f"{Log.FAIL}Fail: {page}{Log.ENDC}")
                logger.info("Retrying...")
                return self.get_movies(page)

            # OK 200?
            if 'status' in conn_result and conn_result['status'] != 'ok':
                return False
            if 'movies' not in conn_result['data']:
                return False
            # Yield result
            return conn_result['data']['movies']

    def pool_request(self):
        """
        Pool async requests for YTS
        :return:
        """
        # Uri
        with self.request() as ping:
            if not 'data' in ping: return False
            total_pages = round(int(ping['data']['movie_count']) / self.YTS_RECURSIVE_LIMIT)
            total_pages = total_pages if self.yts_recursive_page == 0 else self.yts_recursive_page
            logger.info(f"{Log.HEADER}Requesting {str(total_pages)} pages {Log.ENDC}")
            page_list = range(1, total_pages + 1)

            with Pool(POOL_PROCESS) as pool:
                logger.info(f"Preparing processes: {POOL_PROCESS}")
                return pool.map(self.get_movies, list(page_list))

    def __call__(self):
        """
        Start migrate from YTS
        :return:
        """
        # Get data from pool parallel processing
        for movie_meta_iter in self.pool_request():
            if not movie_meta_iter:
                continue

            for movie_meta in movie_meta_iter:
                logger.info('Indexing ' + movie_meta['title'])
                current_imdb_code_set = {movie_meta['imdb_code']}
                public_domain_movie = self.pb_match.intersection(current_imdb_code_set)

                # Rewrite src id
                movie_meta['resource_id'] = movie_meta['id']
                movie_meta['resource_name'] = 'YTS'
                movie_meta['trailer_code'] = movie_meta['yt_trailer_code']
                movie_meta['pdm'] = bool(public_domain_movie)

                del movie_meta['yt_trailer_code']
                del movie_meta['id']
                del movie_meta['state']
                del movie_meta['url']
                # Push indexed movie
                self.yts_movies_indexed[
                    movie_meta['imdb_code']
                ] = movie_meta

        # Return result
        return self.yts_movies_indexed
