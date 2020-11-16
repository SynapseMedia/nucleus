# import os
# import sys
import argparse
import os
# import ipfsapi
import requests
import json
import time
import random
from pathlib import Path
from multiprocessing import Pool

from resource.py.torrents.yts import YTS

__author__ = 'gmena'
if __name__ == '__main__':
    # CLI
    _parser = argparse.ArgumentParser('YTS Torrent Migrate')
    _parser.add_argument('--from', dest='start', default=1, type=int, help='Start page')
    _parser.add_argument('--step', dest='step', default=30, type=int, help='Step page')
    _parser.add_argument('--clean', dest='clean', help='Reset old registry', action='store_true')
    _parser.add_argument('--refresh', dest='remove', help='Refresh movies by imdb', nargs='*')
    _parser.add_argument('--debug', dest='debug', help='Debug after process', action='store_true')
    _parser.add_argument('--sleep', dest='sleep', default=1, type=int, help='Set sleep between requests')
    _root_api = 'http://yts.mx'

    # CLI args
    _args = _parser.parse_args()

    # Initialize yts.ag
    yts = YTS(
        host='%s/api/v2/list_movies.json' % _root_api,
        start=_args.start,
        limit=_args.step
    )

    # Connect API
    # write db
    dir_path = os.path.dirname(os.path.realpath(__file__))
    write_json = dir_path + '/db.json'
    # pibote = dir_path + '/pibote'
    my_i = 0
    movie_collection = []
    movies_error = []
    # https://github.com/ipfs/py-ipfs-api
    # api = ipfsapi.connect('watchit_ipfs', 5001)
    _agents = [
        'Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/21.0',
        'Mozilla/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 Firefox/10.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'
    ]

    # Session keep alive
    # http://docs.python-requests.org/en/master/user/advanced/#request-and-response-objects
    session = requests.Session()


    def recursive_call(_movies_list):
        _rand = random.randint(0, 3)
        for page, movie_meta_iter in _movies_list:
            print('Hola', page)
            if movie_meta_iter:
                for mv in movie_meta_iter:
                    for i, torrent in enumerate(mv['torrents']):
                        print('Waiting', 1, 'second')
                        time.sleep(1)

                        # get fi
                        try:
                            print('Title:', mv['title'])
                            print('Requesting:', torrent['url'])

                            local_dir = dir_path + '/down_torrents/%s_%s_%s' % (mv['imdb_code'],torrent['quality'],torrent['hash'])
                            file_check = Path(local_dir)

                            if not file_check.is_file():
                                # request file
                                response = session.get(torrent['url'], verify=True, timeout=60, headers={
                                    'User-Agent': _agents[_rand]
                                })

                                # Check status for response
                                if response.status_code == requests.codes.ok:
                                    # Avoid to re-download
                                    out = open(local_dir, "wb")
                                    for block in response.iter_content(1024):
                                        if not block:
                                            break
                                        out.write(block)
                                    out.close()
                                else:
                                    print('Bad URL')
                            else:
                                print("Existing file: ", torrent['hash'])

                            # Add file to block-chain
                            # TODO add directory using go ipfs and update links
                            # TODO just download the files and later add it to ipfs using dir
                            # TODO call files {imdb_code}{resolution}{hash}
                            #new_file = api.add(local_dir)
                            torrent['url'] = new_file
                            print(new_file)

                        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
                            print('Bad Torrent')
                            print(mv['title'])
                            print(torrent['url'])
                            print(e)

        with open(write_json, 'w') as outfile:
            json.dump(movie_collection, outfile)
            # api.add(outfile)

    # The result of migration
    pool = Pool(processes=10)
    p_async = pool.apply_async
    for mv in yts.request_generator():
        # Generate async pools
        p_async(recursive_call, args=(mv,))

     # Close pool
    pool.close()
    pool.join()
    print("Total error:", len(movies_error))
    exit()

# export PYTHONPATH=. && python resource/migrate_torrents.py
