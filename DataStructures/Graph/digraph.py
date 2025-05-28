from DataStructures.Map import map_linear_probing as mp
from DataStructures.List import array_list as lt
from DataStructures.Graph import vertex as vtx
from DataStructures.Graph import edge as edg


def new_graph(order):
    return {
        "vertices": mp.newMap(order, 0.5),
        "num_edges": 0,
        "order": order
    }


def insert_vertex(my_graph, key_u, info_u=None):
    if not mp.contains(my_graph["vertices"], key_u):
        vertex = vtx.new_vertex(key_u, info_u)
        mp.put(my_graph["vertices"], key_u, vertex)
    return my_graph


def update_vertex_info(my_graph, key_u, new_info_u):
    if mp.contains(my_graph["vertices"], key_u):
        vertex = mp.get(my_graph["vertices"], key_u)["value"]
        vtx.set_value(vertex, new_info_u)
    return my_graph


def remove_vertex(my_graph, key_u):
    if mp.contains(my_graph["vertices"], key_u):
        mp.remove(my_graph["vertices"], key_u)
    return my_graph


def add_edge(my_graph, key_u, key_v, weight=1.0):
    if not mp.contains(my_graph["vertices"], key_u):
        insert_vertex(my_graph, key_u)
    if not mp.contains(my_graph["vertices"], key_v):
        insert_vertex(my_graph, key_v)

    vertex_u = mp.get(my_graph["vertices"], key_u)["value"]
    vtx.add_adjacent(vertex_u, key_v, weight)
    my_graph["num_edges"] += 1
    return my_graph


def order(my_graph):
    return mp.size(my_graph["vertices"])


def size(my_graph):
    return my_graph["num_edges"]


def vertices(my_graph):
    keys = mp.key_set(my_graph["vertices"])
    vlist = lt.new_list()
    for key in keys:
        lt.add_last(vlist, key)
    return vlist


def degree(my_graph, key_u):
    if not mp.contains(my_graph["vertices"], key_u):
        raise Exception(f"El vértice '{key_u}' no existe en el grafo")
    vertex = mp.get(my_graph["vertices"], key_u)["value"]
    return vtx.degree(vertex)


def get_edge(my_graph, key_u, key_v):
    vertex = get_vertex(my_graph, key_u)
    if vertex:
        return vtx.get_edge(vertex, key_v)
    return None


def get_vertex_information(my_graph, key_u):
    vertex = get_vertex(my_graph, key_u)
    if vertex:
        return vtx.get_value(vertex)
    return None


def contains_vertex(my_graph, key_u):
    return mp.contains(my_graph["vertices"], key_u)


def adjacents(my_graph, key_u):
    vertex = get_vertex(my_graph, key_u)
    if not vertex:
        return lt.new_list()
    adj_map = vtx.get_adjacents(vertex)
    keys = mp.key_set(adj_map)
    result = lt.new_list()
    for key in keys:
        lt.add_last(result, key)
    return result


def edges_vertex(my_graph, key_u):
    vertex = get_vertex(my_graph, key_u)
    if not vertex:
        return lt.new_list()
    adj_map = vtx.get_adjacents(vertex)
    values = mp.value_set(adj_map)
    result = lt.new_list()
    for edge in values:
        lt.add_last(result, edge)
    return result


def get_vertex(my_graph, key_u):
    if mp.contains(my_graph["vertices"], key_u):
        return mp.get(my_graph["vertices"], key_u)["value"]
    return None
