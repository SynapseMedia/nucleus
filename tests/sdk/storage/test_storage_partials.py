import nucleus.sdk.storage as store
from nucleus.sdk.storage import Client


def test_estuary_service_partial():
    """Should return expected estuary client instance"""

    estuary_client = store.estuary('ESTbb693fa8-d758-48ce-9843-a8acadb98a53ARY')
    # should be equal to default meta field + custom fields
    assert isinstance(estuary_client, Client)
