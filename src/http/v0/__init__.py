from src.http.v0.marketplace.movie import *  # noqa
from src.http.v0.marketplace.creator import *  # noqa
from src.http.v0.marketplace.proxy import *  # noqa
from src.http.v0.marketplace.bids import *  # noqa
from src.http.main import app

app.register_blueprint(movie_, url_prefix="/marketplace/movie")  # noqa
app.register_blueprint(bids_, url_prefix="/marketplace/bids")  # noqa
app.register_blueprint(creator_, url_prefix="/marketplace/creator")  # noqa
app.register_blueprint(proxy_, url_prefix="/marketplace/proxy")  # noqa
