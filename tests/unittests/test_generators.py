from gemtest.generators.randfloat import RandFloat


def test_randfloat_min_max():
    randfloat = RandFloat(min_value=1,
                          max_value=3)

    assert randfloat.min_value == 1
    assert randfloat.max_value == 3

    result = randfloat.generate()
    assert result >= 1
    assert result <= 3
    assert isinstance(result, float)
