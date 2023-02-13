import src.sdk.logger as logger
import src.sdk.retrieval as retrieval


mock_collectors_dir = "src/tests/_mock/collectors/"


def test_orbit_subprocess_call():
    """Should run migrate subprocess to expose metadata"""

    with logger.console.status("Migrating.."):
        # Run a subprocess foreach collector to migrate.
        # In this case we are using merge strategy so we expose a batch
        # metadata.
        ipc = retrieval.migrate("--key=dummy", "--c=dummy")()
        stdout = ipc.communicate(b"abc")

        match_logs: list[bool] = []
        expected_matches = ["Waiting for data", "abc"]
        for log in expected_matches:
            match_found = log in stdout.logs
            match_logs.append(match_found)

        assert all(match_logs)