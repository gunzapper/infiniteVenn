"""tests for intersect_and_purge_by_indx."""

from set2net import set2net as s2n
# from hypothesis import given, assume, strategies as st


# @given(
#     st.lists(st.integers(max_value=10, min_value=0)),
#     st.lists(elements=st.iterables(st.characters())), min_size=10)
# def test_result_is_always_less_or_equal_each_set_passed(indexes, all_sets):
#     res = s2n.intersect_and_purge_by_indx(indexes, all_sets)
#     min_len_input_set = min([len(s) for s in all_sets]) if all_sets else 0
#     assert not len(res) > min_len_input_set

def test_intersect_and_purge_by_index():
    sets = [{1, 2}, {2, 3, 4}]
    get = s2n.intersect_and_purge_by_indx([0, 1], sets)
    want = {2}
    assert get == want

