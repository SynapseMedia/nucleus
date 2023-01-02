import src.core.subprocess as subprocess
import src.sdk.harvest.collectors as collectors
import src.sdk.expose.cmd as expose

from src.sdk.harvest.models import Movie

mock_collectors_dir = "src/tests/_mock/collectors/"


def test_orbit_subprocess_call():
    """Should run migrate subprocess to expose metadata"""

    loaded_collectors = collectors.load(mock_collectors_dir)
    data_merged = collectors.merge(loaded_collectors)

    # store metadata in cache
    stored_meta = Movie.batch(data_merged)

    # Run a subprocess foreach collector to migrate
    commands = (expose.migrate(collector) for collector in loaded_collectors)
    subprocess.spawn(commands)

    # TODO store batch merged
    # TODO run sub orbit
