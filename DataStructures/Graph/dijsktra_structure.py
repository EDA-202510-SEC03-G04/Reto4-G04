from DataStructures.Map import map_linear_probing as mp
from DataStructures.Priority_queue import priority_queue as pq
from DataStructures.Graph import edge as e
from DataStructures.Graph import vertex as vtx

def new_dijsktra_structure(source, g_order):
    structure = {
        "source": source,
        "visited": mp.new_map(g_order, 0.5),
        "pq": pq.new_heap()
    }
    return structure


def dijkstra(graph, source):
    structure = new_dijsktra_structure(source, graph["order"])
    mp.put(structure["visited"], source, {
        "distTo": 0,
        "edgeTo": None
    })
    pq.insert(structure["pq"], source, 0)

    while not pq.is_empty(structure["pq"]):
        current = pq.remove_min()
        current_dist = mp.get(structure["visited"], current)["value"]["distTo"]

        for adj_edge in vtx.edges(graph, current):
            neighbor = e.other(graph, adj_edge, current)
            weight = e.weight(graph, adj_edge)
            neighbor_entry = mp.get(structure["visited"], neighbor)

            new_dist = current_dist + weight

            if neighbor_entry is None:
                mp.put(structure["visited"], neighbor, {
                    "distTo": new_dist,
                    "edgeTo": adj_edge
                })
                pq.insert(structure["pq"], neighbor, new_dist)
            else:
                if new_dist < neighbor_entry["value"]["distTo"]:
                    mp.put(structure["visited"], neighbor, {
                        "distTo": new_dist,
                        "edgeTo": adj_edge
                    })
                    pq.decrease_key(structure["pq"], neighbor, new_dist)

    return structure


def has_path_to(structure, vertex):
    entry = mp.get(structure["visited"], vertex)
    return entry is not None and entry["value"]["distTo"] < float('inf')


def distance_to(structure, vertex):
    entry = mp.get(structure["visited"], vertex)
    return entry["value"]["distTo"] if entry else float('inf')


def path_to(structure, vertex):
    if not has_path_to(structure, vertex):
        return []

    path = []
    current = vertex
    while current != structure["source"]:
        entry = mp.get(structure["visited"], current)
        edge = entry["value"]["edgeTo"]
        path.insert(0, edge)
        current = e.other(None, edge, current) 

    return path

