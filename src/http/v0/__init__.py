from .cache import *  # noqa
from .proxy import *  # noqa
from src.http.main import app
app.register_blueprint(cache_, url_prefix='/cache')
app.register_blueprint(proxy_, url_prefix='/proxy')
