from ...scheme.merge import reduce_gens


# Unit tests
def test_reduce_gens():
    """Should reduce generators list to one only"""
    gen_a = ([0, 1, 2],)
    gen_b = ([3, 4, 5],)
    gen_c = ([6, 7, 8],)
    expected = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    assert reduce_gens((gen_a, gen_b, gen_c)) == expected
