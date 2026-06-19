import pytest
from hypothesis import given, assume
from hypothesis import strategies as st
from utils import clamp, merge_sorted, parse_pair, unique_sorted

def test_clamp_basic():
    assert clamp(5, 1, 10) == 5
    assert clamp(0, 1, 10) == 1
    assert clamp(15, 1, 10) == 10
    assert clamp(1, 1, 10) == 1
    assert clamp(5, 5, 5) == 5

def test_merge_sorted_basic():
    assert merge_sorted([1, 3, 5], [2, 4, 6]) == [1, 2, 3, 4, 5, 6]
    assert merge_sorted([], [1, 2]) == [1, 2]
    assert merge_sorted([1, 1], [1, 2]) == [1, 1, 1, 2]

def test_parse_pair_cases():
    assert parse_pair("1:2") == (1, 2)
    with pytest.raises(ValueError):
        parse_pair("hello")
    with pytest.raises(ValueError):
        parse_pair("1:2:3")

def test_unique_sorted_bug():
    input_data = [1, 1, 1]
    assert unique_sorted(input_data) == [1]

@given(st.integers(), st.integers(), st.integers())
def test_clamp_properties(x, lo, hi):
    assume(lo <= hi)
    res = clamp(x, lo, hi)
    assert lo <= res <= hi
    assert clamp(res, lo, hi) == res

sorted_lists = st.lists(st.integers()).map(sorted)

@given(sorted_lists, sorted_lists)
def test_merge_sorted_properties(a, b):
    res = merge_sorted(a, b)
    assert res == sorted(res)
    assert len(res) == len(a) + len(b)
    assert sorted(res) == sorted(a + b)
