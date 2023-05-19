import json

import pytest
import responses

from nucleus.core.types import Any


def _bind_request(mock_link: str, expected_output: str, **kwargs: Any):
    responses.add(
        responses.POST,
        mock_link,
        **{
            **{
                'body': expected_output,
                'status': 200,
            },
            **kwargs,
        },
    )

    return json.loads(expected_output)


@pytest.fixture()
def rpc_api_block_put_request(**kwargs: Any):
    mock_link = (
        'http://localhost:5001/api/v0/block/put?mhtype=sha2-256&mhlen=-1&pin=True&cid-codec=cidv2&allow-big-block=False'
    )
    expected_output = '{"Key": "bafyjvzacdjrk37kqvy5hbqepmcraz3txt3igs7dbjwwhlfm3433a", "Size": "197"}'
    return _bind_request(mock_link, expected_output)
