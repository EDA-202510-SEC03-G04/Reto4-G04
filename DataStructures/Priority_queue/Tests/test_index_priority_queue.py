from DataStructures.Priority_queue import index_priority_queue as pq
from DataStructures.Map import map_linear_probing as mp
from DataStructures.List import array_list as lt


def setup_tests():
    empty_index = pq.new_index_heap()

    some_index = pq.new_index_heap()

    for i in range(1, 14, 2):
        lt.add_last(some_index["elements"], {"key": i, "index": i})
        mp.put(some_index["qp_map"], i, (i // 2) + 1)
        some_index["size"] += 1

    return empty_index, some_index


def test_new_index_heap():
    new_index = pq.new_index_heap()

    assert new_index is not None
    assert new_index["size"] == 0
    assert new_index["elements"] is not None
    assert new_index["elements"]["size"] == 1
    assert new_index["elements"]["elements"] == [None]
    assert new_index["cmp_function"] == pq.cmp_function_lower_value
    assert new_index["qp_map"]["type"] == "PROBING"
    assert new_index["qp_map"]["capacity"] == 211

    new_index = pq.new_index_heap(False)
    assert new_index is not None
    assert new_index["size"] == 0
    assert new_index["elements"] is not None
    assert new_index["elements"]["size"] == 1
    assert new_index["elements"]["elements"] == [None]
    assert new_index["cmp_function"] == pq.cmp_function_higher_value
    assert new_index["qp_map"]["type"] == "PROBING"
    assert new_index["qp_map"]["capacity"] == 211


def test_cmp_function_lower_value():

    assert (
        pq.cmp_function_lower_value(
            {"key": 1, "index": 1}, {"key": 1, "index": 1})
        == True
    )
    assert (
        pq.cmp_function_lower_value(
            {"key": 1, "index": 1}, {"key": 2, "index": 2})
        == True
    )
    assert (
        pq.cmp_function_lower_value(
            {"key": 2, "index": 2}, {"key": 1, "index": 1})
        == False
    )


def test_cmp_function_higher_value():
    assert (
        pq.cmp_function_higher_value(
            {"key": 1, "index": 1}, {"key": 1, "index": 1})
        == True
    )
    assert (
        pq.cmp_function_higher_value(
            {"key": 1, "index": 1}, {"key": 2, "index": 2})
        == False
    )
    assert (
        pq.cmp_function_higher_value(
            {"key": 2, "index": 2}, {"key": 1, "index": 1})
        == True
    )


def test_insert():
    empty_index, some_index = setup_tests()

    pq.insert(empty_index, 1, 1)
    assert empty_index["size"] == 1
    assert empty_index["elements"]["size"] == 2
    assert empty_index["elements"]["elements"][1]["key"] == 1
    assert empty_index["elements"]["elements"][1]["index"] == 1
    assert empty_index["elements"]["elements"][0] is None

    pq.insert(some_index, 2, 2)
    assert some_index["size"] == 8
    assert some_index["elements"]["elements"] == [
        None,
        {"key": 1, "index": 1},
        {"key": 2, "index": 2},
        {"key": 5, "index": 5},
        {"key": 3, "index": 3},
        {"key": 9, "index": 9},
        {"key": 11, "index": 11},
        {"key": 13, "index": 13},
        {"key": 7, "index": 7},
    ]

    pq.insert(some_index, 4, 4)
    assert some_index["size"] == 9
    assert some_index["elements"]["elements"] == [
        None,
        {"key": 1, "index": 1},
        {"key": 2, "index": 2},
        {"key": 5, "index": 5},
        {"key": 3, "index": 3},
        {"key": 9, "index": 9},
        {"key": 11, "index": 11},
        {"key": 13, "index": 13},
        {"key": 7, "index": 7},
        {"key": 4, "index": 4},
    ]


def test_is_empty():
    empty_index, some_index = setup_tests()

    assert pq.is_empty(empty_index) == True
    assert pq.is_empty(some_index) == False


def test_size():
    empty_index, some_index = setup_tests()

    assert pq.size(empty_index) == 0
    assert pq.size(some_index) == 7


def test_contains():
    empty_index, some_index = setup_tests()

    assert pq.contains(empty_index, 1) == False

    assert pq.contains(some_index, 1) == True
    assert pq.contains(some_index, 2) == False


def test_get_first_priority():
    empty_index, some_index = setup_tests()

    assert pq.get_first_priority(empty_index) == None
    assert pq.get_first_priority(some_index) == 1
    assert some_index["size"] == 7

    pq.insert(some_index, 0, 0)

    assert pq.get_first_priority(some_index) == 0
    assert some_index["size"] == 8


def test_remove():
    empty_index, some_index = setup_tests()

    assert pq.remove(empty_index) == None

    response = pq.remove(some_index)

    assert response == 1
    assert some_index["size"] == 6
    assert some_index["elements"]["elements"] == [
        None,
        {"key": 3, "index": 3},
        {"key": 7, "index": 7},
        {"key": 5, "index": 5},
        {"key": 13, "index": 13},
        {"key": 9, "index": 9},
        {"key": 11, "index": 11},
    ]


def test_decrese_key():
    empty_index, some_index = setup_tests()

    pq.decrease_key(some_index, 5, 0)

    assert some_index["size"] == 7
    assert some_index["elements"]["size"] == 8
    assert some_index["elements"]["elements"] == [
        None,
        {"key": 5, "index": 0},
        {"key": 3, "index": 3},
        {"key": 1, "index": 1},
        {"key": 7, "index": 7},
        {"key": 9, "index": 9},
        {"key": 11, "index": 11},
        {"key": 13, "index": 13},
    ]

    pq.decrease_key(some_index, 7, -1)

    assert some_index["size"] == 7
    assert some_index["elements"]["size"] == 8
    assert some_index["elements"]["elements"] == [
        None,
        {"key": 7, "index": -1},
        {"key": 5, "index": 0},
        {"key": 1, "index": 1},
        {"key": 3, "index": 3},
        {"key": 9, "index": 9},
        {"key": 11, "index": 11},
        {"key": 13, "index": 13},
    ]


def test_increase_key():
    empty_index, some_index = setup_tests()

    pq.increase_key(some_index, 5, 15)

    assert some_index["size"] == 7
    assert some_index["elements"]["size"] == 8
    assert some_index["elements"]["elements"] == [
        None,
        {"key": 1, "index": 1},
        {"key": 3, "index": 3},
        {"key": 11, "index": 11},
        {"key": 7, "index": 7},
        {"key": 9, "index": 9},
        {"key": 5, "index": 15},
        {"key": 13, "index": 13},
    ]

    pq.increase_key(some_index, 3, 17)

    assert some_index["size"] == 7
    assert some_index["elements"]["size"] == 8
    assert some_index["elements"]["elements"] == [
        None,
        {"key": 1, "index": 1},
        {"key": 7, "index": 7},
        {"key": 11, "index": 11},
        {"key": 3, "index": 17},
        {"key": 9, "index": 9},
        {"key": 5, "index": 15},
        {"key": 13, "index": 13},
    ]
