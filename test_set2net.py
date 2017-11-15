'''test for set2net.'''

from copy import deepcopy

import set2net as s2n


def test_purge_simple():
    '''basic test'''
    result = s2n.purge({0, 1, 2, 3, 4, 5}, [{0, 1, 2}, {1, 2, 3}, {2, 3, 4}])
    assert result == {5}
    result = s2n.purge({0, 1, 2, 3, 4}, [{0, 1, 2}, {1, 2, 3}, {2, 3, 4}])
    assert result == set()


def test_purge_other_sets_no_change():
    '''testing that at the end of computation other_sets does not change'''

    other_sets = [{0, 1, 2}, {1, 2, 3}, {2, 3, 4}]
    copy_of_other_sets = deepcopy(other_sets)
    assert other_sets == copy_of_other_sets
    assert other_sets is not copy_of_other_sets

    s2n.purge({0, 1, 2, 3, 4, 5}, other_sets)
    assert other_sets == copy_of_other_sets
