import os
import pytest
from unittest import mock

PINATA_SERVICE = "pinata"
PINATA_ENDPOINT = "https://api.pinata.cloud"
WALLET_KEY = "8da4ef21b864d2cc526dbdb2a120bd2874c36c9d0a1fb7f8c63d7f7a8b41de8f"


@pytest.fixture(autouse=True)
def mock_var_env():
    with mock.patch.dict(
        os.environ,
        {
            "PINATA_SERVICE": PINATA_SERVICE,
            "PINATA_ENDPOINT": PINATA_ENDPOINT,
            "WALLET_KEY": WALLET_KEY,
        },
    ):
        yield


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    test_fn = item.obj
    docstring = getattr(test_fn, "__doc__")
    if docstring:
        report.nodeid = docstring
