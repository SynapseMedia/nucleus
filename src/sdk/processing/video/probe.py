# import ffmpeg  # type: ignore

# from src.core.types import Path, Dict, Any

# TODO crear clase ffmpeg  probe
# TODO comprobar si el formato existe en el origen FFProbe para HLS y DASH verificar primero
# TODO el codec que tiene el original si no es diferente al de salida solo copiar


# class FFProbe(object):

#     _raw: Dict[Any, Any]

#     def __init__(self, path: Path):
#         self._raw = ffmpeg.probe(path)  # type: ignore

    
#     def __getattr__(self, name: str) -> Any:
#         """Dynamic access to dict fields
        
#         :param name: the expected index to 
#         """

# def probe(self, **kwargs: Any) -> Any:
#     """Delegate call to underlying lib with context input path"""
#     path = self._library.node.kwargs.get("filename", "")  # type: ignore
#     return ffmpeg.probe(path, **kwargs)  # type: ignore
