from DataStructures.Priority_queue import priority_queue as pq
from DataStructures.List import array_list as lt


def setup_tests():
    empty_heap = pq.new_heap()

    some_heap = pq.new_heap()

    for i in range(1, 14, 2):
        lt.add_last(some_heap["elements"], {"key": i, "value": i})
        some_heap["size"] += 1

    return empty_heap, some_heap


def test_new_heap():
    new_heap = pq.new_heap()

    assert new_heap is not None
    assert new_heap["size"] == 0
    assert new_heap["elements"] is not None
    assert new_heap["elements"]["size"] == 1
    assert new_heap["elements"]["elements"] == [None]
    assert new_heap["cmp_function"] == pq.cmp_function_lower_value

    new_heap = pq.new_heap(False)
    assert new_heap is not None
    assert new_heap["size"] == 0
    assert new_heap["elements"] is not None
    assert new_heap["elements"]["size"] == 1
    assert new_heap["elements"]["elements"] == [None]
    assert new_heap["cmp_function"] == pq.cmp_function_higher_value


def test_cmp_function_lower_value():

    assert (
        pq.cmp_function_lower_value(
            {"key": 1, "value": 1}, {"key": 1, "value": 1})
        == True
    )
    assert (
        pq.cmp_function_lower_value(
            {"key": 1, "value": 1}, {"key": 2, "value": 2})
        == True
    )
    assert (
        pq.cmp_function_lower_value(
            {"key": 2, "value": 2}, {"key": 1, "value": 1})
        == False
    )


def test_cmp_function_higher_value():
    assert (
        pq.cmp_function_higher_value(
            {"key": 1, "value": 1}, {"key": 1, "value": 1})
        == True
    )
    assert (
        pq.cmp_function_higher_value(
            {"key": 1, "value": 1}, {"key": 2, "value": 2})
        == False
    )
    assert (
        pq.cmp_function_higher_value(
            {"key": 2, "value": 2}, {"key": 1, "value": 1})
        == True
    )


def test_insert():
    empty_heap, some_heap = setup_tests()

    pq.insert(empty_heap, 1, 1)
    assert empty_heap["size"] == 1
    assert empty_heap["elements"]["elements"][1]["key"] == 1
    assert empty_heap["elements"]["elements"][1]["value"] == 1
    assert empty_heap["elements"]["elements"][0] is None

    pq.insert(some_heap, 2, 2)
    assert some_heap["size"] == 8
    assert some_heap["elements"]["elements"] == [
        None,
        {"key": 1, "value": 1},
        {"key": 2, "value": 2},
        {"key": 5, "value": 5},
        {"key": 3, "value": 3},
        {"key": 9, "value": 9},
        {"key": 11, "value": 11},
        {"key": 13, "value": 13},
        {"key": 7, "value": 7},
    ]

    pq.insert(some_heap, 4, 4)
    assert some_heap["size"] == 9
    assert some_heap["elements"]["elements"] == [
        None,
        {"key": 1, "value": 1},
        {"key": 2, "value": 2},
        {"key": 5, "value": 5},
        {"key": 3, "value": 3},
        {"key": 9, "value": 9},
        {"key": 11, "value": 11},
        {"key": 13, "value": 13},
        {"key": 7, "value": 7},
        {"key": 4, "value": 4},
    ]


def test_is_empty():
    empty_heap, some_heap = setup_tests()
    assert pq.is_empty(empty_heap) == True
    assert pq.is_empty(some_heap) == False


def test_size():
    empty_heap, some_heap = setup_tests()
    assert pq.size(empty_heap) == 0
    assert pq.size(some_heap) == 7


def test_get_first_priority():
    empty_heap, some_heap = setup_tests()

    assert pq.get_first_priority(empty_heap) == None
    assert pq.get_first_priority(some_heap) == 1
    assert some_heap["size"] == 7

    pq.insert(some_heap, 0, 0)

    assert pq.get_first_priority(some_heap) == 0
    assert some_heap["size"] == 8


def test_remove():
    empty_heap, some_heap = setup_tests()

    assert pq.remove(empty_heap) == None

    response = pq.remove(some_heap)

    assert response == 1
    assert some_heap["size"] == 6
    assert some_heap["elements"]["elements"] == [
        None,
        {"key": 3, "value": 3},
        {"key": 7, "value": 7},
        {"key": 5, "value": 5},
        {"key": 13, "value": 13},
        {"key": 9, "value": 9},
        {"key": 11, "value": 11},
    ]
