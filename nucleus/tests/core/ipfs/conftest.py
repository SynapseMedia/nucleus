import responses
import pytest
import json

from nucleus.core.types import Any


@pytest.fixture()
def api_add_request_output(**kwargs: Any):
    mock_link = "http://localhost:5001/api/v0/add?pin=False&quieter=True&hash=blake2b-208&cid_version=1"
    expected_output = '{"Hash": "bafyjvzacdjrk37kqvy5hbqepmcraz3txt3igs7dbjwwhlfm3433a", "Name": "video.mp4", "Size": "17843027"}'

    responses.add(
        responses.POST,
        mock_link,
        **{
            **{
                "body": expected_output,
                "status": 200,
            },
            **kwargs,
        },
    )

    return json.loads(expected_output)
