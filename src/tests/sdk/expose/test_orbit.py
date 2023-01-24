import src.sdk.logger as logger
import src.sdk.harvest as harvest
import src.sdk.expose as expose


mock_collectors_dir = "src/tests/_mock/collectors/"


def test_orbit_subprocess_call():
    """Should run migrate subprocess to expose metadata"""

    with logger.console.status("Harvesting"):
        loaded_collectors = harvest.load(mock_collectors_dir)
        batch_collected = harvest.merge(loaded_collectors)  # strategy
        saved = harvest.batch_save(batch_collected)

    with logger.console.status("Migrating.."):
        # Run a subprocess foreach collector to migrate
        # In this case we are using merge strategy so we expose a batch metadata.
        commands = map(expose.migrate, loaded_collectors)
        process = tuple(commands)[0]()
        stdin, stderr = process.communicate("abc")
        assert 0

    assert all(saved) == True
    """
        just make sure your debug output is rrreeaaalllly good on that migrate node process :D
        and optionally that your python knows how to parse it
    """
    # TODO agregar un proceso intermedio para interceptar los logs de subprocess y poder tomar decisiones respecto a dichos logs. eg: log error, info, etc
    # TODO run sub orbit
    # TODO run sub orbit with map strategy
