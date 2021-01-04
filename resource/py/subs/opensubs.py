import time, os

from collections import defaultdict
from pythonopensubtitles.opensubtitles import OpenSubtitles
from xmlrpc.client import ProtocolError

__author__ = 'gmena'

OPEN_SUBS_RECURSIVE_SLEEP_REQUEST = int(os.environ.get('OPEN_SUBS_RECURSIVE_SLEEP_REQUEST'))
engine = OpenSubtitles('en', 'zorrillosdev')

def login():
    try:
        print('Login to open-sub')
        return engine.login('gmjun2000@gmail.com', 'gmena5289')
    except (ProtocolError, Exception) as e:
        print('Retry login')
        print("\n\033[93mWait", str(OPEN_SUBS_RECURSIVE_SLEEP_REQUEST), 'seconds\033[0m\n')
        time.sleep(OPEN_SUBS_RECURSIVE_SLEEP_REQUEST)
        return login()


def requests_subs(imdb_id: str):
    """
    Request to open sub
    :param imdb_id:
    :return:
    """
    print("\033[92mRequesting rpc open-sub", imdb_id, '\033[0m')
    try:
        _result = engine.search_subtitles([{
            'imdbid': imdb_id.replace('tt', '')
        }])
        _result_set = defaultdict(list)

        for res in _result:
#             print(_result)
            _lang = res['LanguageName'].lower()
            _format = res['InfoFormat'].lower()
            _rate = int(float(res['SubRating']))
            _link = res['ZipDownloadLink']
            _votes = res['SubSumVotes']
            _download = res['SubDownloadsCnt']
            _score = res['Score']
            _trusted = res['SubFromTrusted']
            _result_set[_lang].append({
                'id': res.get('IDSubtitleFile'),
                'rating': _rate,
                'link': _link,
                'format': _format,
                'source': 'opensubtitles',
                'votes': _votes,
                'score': _score,
                'trusted': _trusted,
                'dcount': _download
            })

        return _result_set
    except ProtocolError as e:
         print("\n\033[93mWait", str(OPEN_SUBS_RECURSIVE_SLEEP_REQUEST * 2), 'seconds\033[0m\n')
         time.sleep(OPEN_SUBS_RECURSIVE_SLEEP_REQUEST * 2)
         return requests_subs(imdb_id)
    except (TypeError, Exception) as e:
        print(e)
        print('No sub')
        return {}


def migrate(movies: iter):
    login()

    # Subs lists
    _subs_lists_result = {}

    # Subs lists
    count = 0
    results = {}
    total = movies.count()
    _subs_lists_result = {}

    # Generate async pools
    for data in movies:
        count += 1
        print(data['imdb_code'])
        print((count / total) * 100)
        k = data['imdb_code']
        results[k] = requests_subs(k)

    engine.logout()
    # return list of subs
    return results
