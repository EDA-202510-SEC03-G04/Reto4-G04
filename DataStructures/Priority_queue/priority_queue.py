from DataStructures.List import array_list as lt


def new_heap(is_min_pq=True):
    return {
        'elements': [],
        'is_min_pq': is_min_pq,
        'size': 0,
        'cmp_function': default_compare_lower_value if is_min_pq else default_compare_higher_value
    }


def default_compare_higher_value(father_node, child_node):
    return father_node[0] < child_node[0]


def default_compare_lower_value(father_node, child_node):
    return father_node[0] > child_node[0]

def priority(my_heap, parent, child=None):
    return my_heap['elements'][parent][0]


def insert(my_heap, value, key):
    pair = (key, value)
    my_heap['elements'].append(pair)
    my_heap['size'] += 1
    swim(my_heap, len(my_heap['elements']) - 1)


def size(my_heap):
    return my_heap['size']


def is_empty(my_heap):
    return size(my_heap) == 0

def get_first_priority(my_heap):
    if is_empty(my_heap) or not my_heap['elements']:
        return None
    return my_heap['elements'][0][1]  # el test espera el value, no la tupla


def remove(my_heap):
    if is_empty(my_heap) or not my_heap['elements']:
        return None

    elements = my_heap['elements']
    elements[0], elements[-1] = elements[-1], elements[0]
    removed = elements.pop()
    my_heap['size'] -= 1
    sink(my_heap, 0)
    return removed


def swim(my_heap, pos):
    elements = my_heap['elements']
    is_min_pq = my_heap['is_min_pq']
    while pos > 0:
        parent = (pos - 1) // 2
        if is_min_pq:
            if default_compare_lower_value(elements[parent], elements[pos]):
                elements[pos], elements[parent] = elements[parent], elements[pos]
                pos = parent
            else:
                break
        else:
            if default_compare_higher_value(elements[parent], elements[pos]):
                elements[pos], elements[parent] = elements[parent], elements[pos]
                pos = parent
            else:
                break


def sink(my_heap, pos):
    elements = my_heap['elements']
    is_min_pq = my_heap['is_min_pq']
    n = len(elements)
    while True:
        left = 2 * pos + 1
        right = 2 * pos + 2
        target = pos

        if left < n:
            if is_min_pq:
                if default_compare_lower_value(elements[target], elements[left]):
                    target = left
            else:
                if default_compare_higher_value(elements[target], elements[left]):
                    target = left

        if right < n:
            if is_min_pq:
                if default_compare_lower_value(elements[target], elements[right]):
                    target = right
            else:
                if default_compare_higher_value(elements[target], elements[right]):
                    target = right

        if target != pos:
            elements[pos], elements[target] = elements[target], elements[pos]
            pos = target
        else:
            break