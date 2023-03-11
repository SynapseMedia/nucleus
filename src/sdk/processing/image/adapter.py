from PIL.Image import Image as Pillow
from src.core.types import Adapter


class PillowAdapter(Adapter[Pillow]):
    """Pillow adapter class implements methods to handle PIL at a low level."""
    
    def __instancecheck__(self, instance: Pillow):
        """Override instance check since we need to check subclass for pillow.
        In this case we always receive instance as Pillow (Image) but the _input could be any derived class plugin eg. JpegImage, etc
        so we check inverse validation to know if the expected _input is derived from instance to check (Image).
        
        ref: http://code.nabla.net/doc/PIL/api/PIL/JpegImagePlugin/PIL.JpegImagePlugin.JpegImageFile.html
        """
        return issubclass(self._input.__class__, instance.__class__)
    
    def __getattr__(self, name: str):
        """Delegate calls to underlying lib.
        ref: https://pillow.readthedocs.io/en/stable/reference/Image.html
        """
        return getattr(self._input, name)
