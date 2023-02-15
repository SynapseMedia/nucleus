from src.core.fs import Path
from .types import Engine

class VideoEngine(Engine):
    
    def __enter__(self, path: Path):
        
        ...

    def __exit__(self):
        ...

class ImageEngine:
    ...
