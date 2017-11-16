'''test for set2net.'''

from itertools import permutations
import random
from copy import deepcopy
import string

import pytest

import set2net as s2n


def test_purge_simple():
    '''basic test'''
    result = s2n.purge({0, 1, 2, 3, 4, 5}, [{0, 1, 2}, {1, 2, 3}, {2, 3, 4}])
    assert result == {5}
    result = s2n.purge({0, 1, 2, 3, 4}, [{0, 1, 2}, {1, 2, 3}, {2, 3, 4}])
    assert result == set()
    result = s2n.purge([], [{0, 1, 2}, {1, 2, 3}, {2, 3, 4}])
    assert result == set()


def test_purge_other_sets_no_change():
    '''testing that at the end of computation other_sets does not change'''

    other_sets = [{0, 1, 2}, {1, 2, 3}, {2, 3, 4}]
    copy_of_other_sets = deepcopy(other_sets)
    assert other_sets == copy_of_other_sets
    assert other_sets is not copy_of_other_sets

    s2n.purge({0, 1, 2, 3, 4, 5}, other_sets)
    assert other_sets == copy_of_other_sets


def test_purge_any_iterable():
    '''test work with any iterable'''
    result = s2n.purge(range(6), [{0, 1, 2}, {1, 2, 3}, {2, 3, 4}])
    assert result == {5}
    result = s2n.purge({0, 1, 2, 3, 4}, [[0, 1, 2], [1, 2, 3], [2, 3, 4, 4]])
    assert result == set()


def test_purge_no():
    '''test not work without iterables'''
    with pytest.raises(TypeError):
        s2n.purge(6, [{0, 1, 2}, {1, 2, 3}, {2, 3, 4}])
    with pytest.raises(TypeError):
        s2n.purge({0, 1, 2, 3, 4}, [0, 1, 2, 1, 2, 3, 2, 3, 4, 4])


def test_purge_torture():
    '''very stressfull intensive test.'''
    for i in range(10):
        my_string = list(string.ascii_uppercase[:i])
        random.shuffle(my_string)
        other_strings = list(permutations(string.ascii_uppercase[:10], 5))
        random.shuffle(other_strings)
        res = s2n.purge(my_string, other_strings)
        assert res == set()
