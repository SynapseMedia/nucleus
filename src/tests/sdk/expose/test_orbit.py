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
        # since we are processing one thread for collector we took the first for test
        ipc = tuple(commands)[0]() 
        stdout = ipc.communicate(b"abc")
        
        # if stdout.exit_code > 0:
        for log in stdout.logs:
            print(log)

    assert all(saved) == True
