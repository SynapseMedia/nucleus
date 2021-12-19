from src.http.v0.marketplace.cache import *  # noqa
from src.http.v0.marketplace.proxy import *  # noqa
from src.http.main import app

app.register_blueprint(cache_, url_prefix="/cache")  # noqa
app.register_blueprint(proxy_, url_prefix="/proxy")  # noqa
