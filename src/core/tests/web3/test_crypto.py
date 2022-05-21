from src.sdk.web3.crypto import to_hex, cid_to_uint256


def test_cid_to_uint256():
    """Should return expected output uint256 in deterministic way from input"""
    current_value = "bafyjvzacdk3rngktzetikg3w2gf7nxvxsq5y4t4xryzijalyazsa"
    expected_value = (
        651268735865305864933405567136027539147782079973983219801233220330061301348
    )
    assert cid_to_uint256(current_value) == expected_value


def test_to_hex():
    """Should return expected output hex in deterministic way from input"""
    current_value = "bafyjvzacdk3rngktzetikg3w2gf7nxvxsq5y4t4xryzijalyazsa"
    expected_value = (
        "0x626166796a767a6163646b33726e676b747a6574696b673"
        "377326766376e787678737135793474347872797a696a616c79617a7361"
    )
    assert to_hex(current_value.encode()) == expected_value
