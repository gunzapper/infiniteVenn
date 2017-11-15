'''test for set2net.'''

import set2net as s2n


def test_purge_simple():
    '''basic test'''
    result = s2n.purge({0, 1, 2, 3, 4, 5}, [{0, 1, 2}, {1, 2, 3}, {2, 3, 4}])
    assert result == {5}
    result = s2n.purge({0, 1, 2, 3, 4}, [{0, 1, 2}, {1, 2, 3}, {2, 3, 4}])
    assert result == {}
