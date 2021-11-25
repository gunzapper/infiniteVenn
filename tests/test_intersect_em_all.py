"""tests for intersect_em_all."""

from set2net import set2net as s2n
from hypothesis import given, assume, strategies as st


def test_intersect_em_all_not_intersection():
    """
        there is not interception
        between {1, 2, 3}, {4, 5} and {3}"""
    result = s2n.intersect_em_all([{1, 2, 3}, {4, 5}, {3}])
    assert result == set()


def test_intersect_em_all_empty():
    """Passing a list of empty sets it should return an empty set"""
    result = s2n.intersect_em_all([set(), set(), set(), set()])
    assert result == set()


def test_there_is_an_interception():
    """Passing a list of empty sets it should return an empty set"""
    result = s2n.intersect_em_all([{1, 2, 3}, {4, 5, 3}, {3}])
    assert result == {3}


@given(st.lists(st.sets(st.characters()), min_size=10))
def test_result_is_always_less_or_equal_each_set_passed(sets):
    res = s2n.intersect_em_all(sets)
    assert len(res) <= min([len(s) for s in sets])
