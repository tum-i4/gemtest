from gemtest.relations import or_
from gemtest.relations.simple import equality, is_less_than, is_greater_than


def test_or_():
    def relation_1(a, b):
        return True

    def relation_2(a, b):
        return False

    assert or_(relation_1, relation_2).__name__ == "relation_1 or relation_2"
    true_true = or_(relation_1, relation_1)
    true_false = or_(relation_1, relation_2)
    false_false = or_(relation_2, relation_2)
    assert true_true(1, 1)
    assert true_false(1, 1)
    assert not false_false(1, 1)


def test_equality():
    assert equality(1, 1)
    assert not equality(1, 2)


def test_is_less_than():
    assert is_less_than(1, 2)
    assert not is_less_than(2, 1)


def test_is_greater_than():
    assert is_greater_than(2, 1)
    assert not is_greater_than(1, 2)
