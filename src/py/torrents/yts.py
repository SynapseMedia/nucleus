import requests
from contextlib import contextmanager
from multiprocessing import Pool

from src.py import Log
from src.py.media.ingest import get_pb_domain_set

__author__ = 'gmena'
POOL_PROCESS = 10
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

    def __init__(self, host: str= ROOT_API, page: int = 0, limit: int = 50):
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
        _request: str = self.YTS_HOST + ('?%s' % query_string if query_string else '')
        _cookie = 'adcashufpv3=17981512371092097718392042062; __cfduid=dbf1c05bdb221675033d2ae958eb4f2961610924444; __atuvc=1%7C3; PHPSESSID=vaddrbb83hnm7sfj1tgqc52shg; __cf_bm=0284cbddd1042cb621f57dd4f36b2d517b13eb50-1610994684-1800-AWmH5PKF0W0T0T2wUzqQ1XOuj7WyhuhPAfuSnF38dBYEyrQ/TQlfb4lT7jds14lU2/5IwLQB2NsIGGFd2rk7GLB85AbgZ1BbEnrV+NuKkyio78/maf1rUB2w5S1qGgnadQ=='
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
            print(e)
            yield {}

    def get_movies(self, page):
        """
        Process request for movies from YTS
        :param page:
        :return:
        """
        # Req YTS
        print(f"Requesting page {str(page)}")
        _uri = 'page=' + str(page) + '&limit=' + str(self.YTS_RECURSIVE_LIMIT) + '&sort=date_added'
        with self.request(_uri) as conn_result:
            # OK 200?
            if 'status' in conn_result and conn_result['status'] != 'ok':
                return False
            if 'movies' not in conn_result['data']:
                return False
            # Yield result
            return conn_result['data']['movies']

    def request_generator(self) -> iter:
        """
        Pool async requests for YTS
        :return:
        """

        # Uri
        with self.request() as ping:
            if not 'data' in ping: return False
            total_pages = round(int(ping['data']['movie_count']) / self.YTS_RECURSIVE_LIMIT)
            total_pages = total_pages if self.yts_recursive_page == 0 else self.yts_recursive_page

            print(f"{Log.HEADER}Requesting {str(total_pages)} pages {Log.ENDC}")
            page_list = range(total_pages)

            with Pool(processes=POOL_PROCESS) as pool:
                p_async = pool.apply_async
                results = {}

                # Generate async pools
                for x in page_list:
                    results[x] = p_async(
                        self.get_movies, args=(x,)
                    )

                # Close pool
                pool.close()
                pool.join()
            # Generate dict with data
            for x, y in results.items():
                yield x, y.get()

    def migrate(self):
        """
        Start migrate from YTS
        :return:
        """
        # Get generator
        for page, movie_meta_iter in self.request_generator():
            if not movie_meta_iter:
                continue
            for movie_meta in movie_meta_iter:
                print('indexing ' + movie_meta['title'])
                current_imdb_code_set = {movie_meta['imdb_code']}
                public_domain_movie = self.pb_match.intersection(current_imdb_code_set)

                # Rewrite src id
                movie_meta['page'] = page
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
