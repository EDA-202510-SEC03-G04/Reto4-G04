from DataStructures.Map import map_linear_probing as mp
from DataStructures.Graph import edge as edg

def new_vertex(key, value):
    vertex = {"key": key, "value": value, "adjacents": mp.newMap(7, 0.5)}
    return vertex

def get_key(vertex):
    return vertex["key"]

def get_value(vertex):
    return vertex["value"]

def set_value(vertex, new_value):
    vertex["value"] = new_value

def get_adjacents(vertex):
    return vertex["adjacents"]

def get_edge(vertex, key_v):
    if mp.contains(vertex["adjacents"], key_v):
        return mp.get(vertex["adjacents"], key_v)["value"]
    return None

def add_adjacent(vertex, key_vertex, weight):
    new_edge = edg.new_edge(key_vertex, weight)
    mp.put(vertex["adjacents"], key_vertex, new_edge)
    return vertex


def degree(vertex):
    return mp.size(vertex["adjacents"])
