import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from contextlib import contextmanager
from multiprocessing import Pool

__author__ = 'gmena'


class YSubs(object):
    def __init__(self, host: str):
        # http://www.yifysubtitles.com/movie-imdb/{imdb_code}
        self.indexed_subs = []
        self.error_subs = []

        # CONSTANTS
        self.YSUBS_HOST = host
        self.YSUBS_DOC_TYPE = 'subtitles'
        self.req_session = requests.Session()

    @contextmanager
    def request(self, query_string) -> iter:
        """
        Handle http request
        :param query_string:
        :return:
        """

        # Request YTS
        _request = self.YSUBS_HOST + '/movie-imdb/' + query_string
        _cookie = '__cfduid=df5835b1fca2e8f5d6b5760acb778327a1606680247; _ga=GA1.2.1426751841.1606680232; __gads=ID=bfd9eb0faf988b08-22e286746eb80003:T=1606680250:RT=1606680250:S=ALNI_MZv5VFqynyKi4dUVEbFef4Ew9TR9A; _gid=GA1.2.323216250.1608055752; _gat_gtag_UA_127397621_1=1; ys-sw=1348'
        _agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'

        # Request
        try:
            conn = self.req_session.get(
                url=_request,
                headers={
                    "content-type": "json",
                     'user-agent': _agent,
                      'cookie': _cookie
                }
            )
            # Return json
            yield conn.text
        except (Exception,) as e:
            print('Retry request sub error:', e)
            yield self.request(query_string)

    def request_scraper(self, imdb_code: str) -> dict:
        """
        Request yts handler
        :param imdb_code
        :return:
        """
        # Uri
        print("\033[92mRequesting yifi-subtitles", imdb_code, '\033[0m')

        # Req YTS
        with self.request(imdb_code) as conn_result:
            try:
                bf4 = BeautifulSoup(conn_result, 'html5lib')
                bf4_table_result = bf4.find('table', class_='other-subs')
                _result_group = defaultdict(list)
            except TypeError as e:
                self.error_subs.append(imdb_code)
                return defaultdict(list)

            # Not table
            if not bf4_table_result:
                self.error_subs.append(imdb_code)
                return _result_group

            # Found subs rows
            bf4_tr_result = bf4_table_result.find_all('tr')

            # Find entries
            _lang_list = [res.find('td', class_='flag-cell') for res in bf4_tr_result]
            _ratings_lists = [res.find('td', class_='rating-cell') for res in bf4_tr_result]
            _link_list = [None if not res else res.find_next_sibling('td') for res in _lang_list]

            # Zipped
            _zipped = zip(list(_ratings_lists), list(_lang_list), list(_link_list))
            self.indexed_subs.append(imdb_code)

            # Group by language
            for res in _zipped:

                # Not valid language
                if not all(res):
                    continue

                # group name
                _group_name = res[1].get_text() \
                    .lower() \
                    .replace(' ', '-') \
                    .replace('/', '-')

                # structuring
                _result_group[_group_name].append({
                    'rating': res[0].get_text(),
                    'link': self.YSUBS_HOST + res[2].find('a').get('href').replace('subtitles', 'subtitle') + '.zip',
                    'source':'yifi'
                })

            # Return list
            return _result_group

    def migrate(self, movies: iter):
        # Subs lists
        results = {}
        _subs_lists_result = {}
        pool = Pool(processes=5)
        p_async = pool.apply_async

        # Generate async pools
        for data in movies:
            k = data['imdb_code']
            results[k] = p_async(
                self.request_scraper, args=(k,)
            )

        # Close pool
        pool.close()
        pool.join()

        # For each movie
        for k, movie in results.items():
            # Get list of subtitles for each movie
            _movie = movie.get()
            _subs_lists_result[k] = _movie

        # return list of subs
        return _subs_lists_result
