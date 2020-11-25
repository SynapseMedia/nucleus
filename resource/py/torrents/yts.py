import requests
from contextlib import contextmanager
from multiprocessing import Pool

from resource.py.media.ingest import ingest_ipfs

__author__ = 'gmena'


class YTS(object):
    def __init__(self, host: str, page: int = 0, limit: int = 50):
        # ignore 400 cause by IndexAlreadyExistsException when creating an index

        # CONSTANTS
        self.YTS_HOST = host
        self.YTS_RECURSIVE_LIMIT = limit  # limit result per page (step)

        self.yts_recursive_page = page  # start page
        self.yts_movies_indexed = dict()  # indexed
        self.req_session = requests.Session()

    @contextmanager
    def request(self, query_string=None):
        """
        Handle http request
        :param query_string:
        :return:
        """
        # Request yifi
        _request: str = self.YTS_HOST + ('?%s' % query_string if query_string else '')
        _cookie = 'adcashufpv3=17981512371092097718392042062; __atuvc=0%7C33%2C0%7C34%2C1%7C35%2C0%7C36%2C1%7C37; __cfduid=d482a2a492e144c0c7ed075d4dcad6ced1601498497; PHPSESSID=072ncmi79u10em13b129jq5n13'
        _agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'

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
        # Req YTS
        print("\033[92mRequesting page", str(page), '\033[0m')
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
        Request yts handler
        :return:
        """

        # Uri
        with self.request() as ping:
            if not 'data' in ping: return False
            total_pages = round(int(ping['data']['movie_count']) / self.YTS_RECURSIVE_LIMIT)
            total_pages = total_pages if self.yts_recursive_page == 0 else self.yts_recursive_page

            print("\033[92mRequesting", str(total_pages), '\033[0m')
            page_list = range(total_pages)
            pool = Pool(processes=10)
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

    @staticmethod
    def ingest_media(mv):

        media_dir = '/%s' % mv['imdb_code']
        image_index = [
            "background_image", "background_image_original",
            "small_cover_image", "medium_cover_image", "large_cover_image"
        ]

        mv = {**mv, **{ # Merge the ingested files
            x: ingest_ipfs(mv[x], "%s/%s.jpg" % (media_dir, x))
            for x in image_index
        }}

        for torrent in mv['torrents']:
            torrent_dir = '/%s/%s/%s' % (media_dir, torrent['quality'], torrent['hash'])
            torrent['hash'] = ingest_ipfs(torrent['url'], torrent_dir)
        return mv

    def migrate(self, resource_name: str):
        """
        Elastic migrate
        :param resource_name:
        :return:
        """
        # Get generator
        for page, movie_meta_iter in self.request_generator():
            if movie_meta_iter:
                for movie_meta in movie_meta_iter:
                    print('indexing ' + movie_meta['title'])
                    # Rewrite resource id
                    movie_meta['page'] = page
                    movie_meta['resource_id'] = movie_meta['id']
                    movie_meta['resource_name'] = resource_name
                    movie_meta['trailer_code'] = movie_meta['yt_trailer_code']
                    movie_meta = YTS.ingest_media(movie_meta)

                    del movie_meta['yt_trailer_code']
                    del movie_meta['id']
                    del movie_meta['state']
                    del movie_meta['url']
                    # Push indexed
                    self.yts_movies_indexed[movie_meta['imdb_code']] = movie_meta

        # Return result
        return self.yts_movies_indexed
