import nucleus.sdk.storage as store
from nucleus.sdk.storage import Service


def test_estuary_service_partial():
    """Should return expected estuary service instance"""

    estuary_service = store.estuary('ESTbb693fa8-d758-48ce-9843-a8acadb98a53ARY')
    # should be equal to default meta field + custom fields
    assert isinstance(estuary_service, Service)
