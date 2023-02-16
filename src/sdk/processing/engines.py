
from src.sdk.harvest import Media

from .types import Engine

# TODO  eg. Video define all the instructions needed to process it
# class VideoEngine(Engine):


#     def __init__(self, media: Proxy):
#         ...

#     def __enter__(self):

#         ...

#     def __call__(self, **ins: Any):
#         ...

#     def __exit__(self):
#         ...

# class ImageEngine:
#     ...


# TODO desde el modelo obtener los Media -> filtrar los tipos y definir con que engine procesarlo
# TODO se debe omitir de los media los routes que sean CID
# TODO los routes se deben determinar por medio del "fetch" handler para enviarlos a RAW_DIR
# TODO desde RAW_DIR se deben ingresar al engine, donde se guardara el output en PROD_DIR 
# TODO PROD_DIR = un directorio nombrado como el hash unico donde se almacenan todo los resultados (index.json, media, etc)

def process_as(media: Media, engine: Engine):
    ...
