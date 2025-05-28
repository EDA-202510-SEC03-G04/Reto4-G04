import time
import csv
from DataStructures.Graph import digraph as G
from DataStructures.List import array_list as lt
from DataStructures.Map import map_linear_probing as mp
from DataStructures.Priority_queue import priority_queue as pq
from DataStructures.Graph import vertex as vtx
from math import radians, sin, cos, sqrt, atan2


def new_logic():
    """
    Crea el catálogo para almacenar las estructuras de datos
    """
    catalog = {
        "graph": G.new_graph(1000),
        "last_delivery_by_person": mp.newMap(100, 0.5),
        "total_deliveries": 0,
        "total_time": 0,
        "unique_restaurants": lt.new_list(),
        "unique_destinations": lt.new_list(),
        "delivery_people": lt.new_list()
    }
    return catalog


# Funciones para la carga de datos

def default_cmp(a, b):
    return 0 if a == b else -1

def format_coord(lat, lon):
    return f"{float(lat):.4f}_{float(lon):.4f}"


def is_in_list(lst, element):
    return lt.is_present(lst, element, default_cmp) != -1

def add_if_not_present(lst, element):
    if not is_in_list(lst, element):
        lt.add_last(lst, element)

def add_delivery_person_to_node(graph, node_key, person_id):
    vertex = G.get_vertex(graph, node_key)
    if vertex:
        info = vtx.get_value(vertex)
        if info is None:
            info = mp.newMap(10, 0.5)
        if not mp.contains(info, "domiciliarios"):
            mp.put(info, "domiciliarios", lt.new_list())
        dom_list = mp.get(info, "domiciliarios")["value"]
        add_if_not_present(dom_list, person_id)
        mp.put(info, "domiciliarios", dom_list)
        vtx.set_value(vertex, info)
        G.update_vertex_info(graph, node_key, info)


def load_data(catalog, filename):
    graph = catalog["graph"]
    last_by_person = catalog["last_delivery_by_person"]

    with open(filename, encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                person_id = row["Delivery_person_ID"]
                restaurant = format_coord(row["Restaurant_latitude"], row["Restaurant_longitude"])
                destination = format_coord(row["Delivery_location_latitude"], row["Delivery_location_longitude"])
                time_taken = float(row["Time_taken(min)"].strip())
            except:
                continue

            if restaurant == destination:
                continue

            catalog["total_deliveries"] += 1
            catalog["total_time"] += time_taken

            add_if_not_present(catalog["delivery_people"], person_id)
            add_if_not_present(catalog["unique_restaurants"], restaurant)
            add_if_not_present(catalog["unique_destinations"], destination)

            # Insertar vértices con tipo
            rest_info = mp.newMap(10, 0.5)
            mp.put(rest_info, "tipo", "restaurante")
            dest_info = mp.newMap(10, 0.5)
            mp.put(dest_info, "tipo", "destino")

            G.insert_vertex(graph, restaurant, rest_info)
            G.insert_vertex(graph, destination, dest_info)

            # Arista principal
            existing_edge = G.get_edge(graph, restaurant, destination)
            if existing_edge:
                old_weight = existing_edge["weight"]
                new_weight = (old_weight + time_taken) / 2
                G.add_edge(graph, restaurant, destination, new_weight)
            else:
                G.add_edge(graph, restaurant, destination, time_taken)

            # Registrar domiciliario
            add_delivery_person_to_node(graph, restaurant, person_id)
            add_delivery_person_to_node(graph, destination, person_id)

            # Enlazar ubicaciones previas del domiciliario
            last_dest_record = mp.get(last_by_person, person_id)
            if last_dest_record:
                last_dest = last_dest_record["value"]
                if last_dest != destination:
                    G.insert_vertex(graph, last_dest, mp.newMap(10, 0.5))
                    edge_btwn_dests = G.get_edge(graph, last_dest, destination)
                    if edge_btwn_dests:
                        old_weight = edge_btwn_dests["weight"]
                        new_weight = (old_weight + time_taken) / 2
                        G.add_edge(graph, last_dest, destination, new_weight)
                    else:
                        G.add_edge(graph, last_dest, destination, time_taken)
            mp.put(last_by_person, person_id, destination)

    resumen = {
        "n_domicilios": catalog["total_deliveries"],
        "n_domiciliarios": lt.size(catalog["delivery_people"]),
        "n_vertices": G.order(catalog["graph"]),
        "n_aristas": G.size(catalog["graph"]),
        "n_restaurantes": lt.size(catalog["unique_restaurants"]),
        "n_destinos": lt.size(catalog["unique_destinations"]),
        "tiempo_promedio": round(catalog["total_time"] / catalog["total_deliveries"], 2) if catalog["total_deliveries"] > 0 else 0
    }

    return resumen



# Funciones de consulta sobre el catálogo



def req_1(catalog, origen, destino):
    start_time = get_time()
    graph = catalog["graph"]
    visited = lt.new_list()
    path = lt.new_list()

    def dfs(current):
        if current == destino:
            lt.add_last(path, current)
            return True
        lt.add_last(visited, current)
        lt.add_last(path, current)

        adjs = G.adjacents(graph, current)
        for i in range(lt.size(adjs)):
            adj = lt.get_element(adjs, i)
            if not is_in_list(visited, adj):
                if dfs(adj):
                    return True
        lt.remove_last(path)
        return False

    found = dfs(origen)
    end_time = get_time()

    if not found:
        return {"existe": False, "tiempo": delta_time(start_time, end_time)}

    domiciliarios = lt.new_list()
    restaurantes = lt.new_list()
    for i in range(lt.size(path)):
        nodo = lt.get_element(path, i)
        info = G.get_vertex_information(graph, nodo)
        if info and mp.contains(info, "domiciliarios"):
            doms = mp.get(info, "domiciliarios")["value"]
            for j in range(lt.size(doms)):
                dom = lt.get_element(doms, j)
                add_if_not_present(domiciliarios, dom)
        if info and mp.contains(info, "tipo"):
            tipo = mp.get(info, "tipo")["value"]
            if tipo == "restaurante":
                add_if_not_present(restaurantes, nodo)

    return {
        "existe": True,
        "tiempo": delta_time(start_time, end_time),
        "num_puntos": lt.size(path),
        "camino": path,
        "domiciliarios": domiciliarios,
        "restaurantes": restaurantes
    }


def req_2(catalog, origen, destino, domiciliario):
    start_time = get_time()
    graph = catalog["graph"]
    visited = lt.new_list()
    parent = mp.newMap(100, 0.5)
    dist = mp.newMap(100, 0.5)
    heap = pq.new_heap(is_min_pq=True)

    pq.insert(heap, origen, 0)
    mp.put(dist, origen, 0)

    found = False

    while not pq.is_empty(heap):
        current = pq.remove(heap)[1]
        current_dist = mp.get(dist, current)["value"]

        if current == destino:
            found = True
            break

        add_if_not_present(visited, current)

        adjs = G.adjacents(graph, current)
        for i in range(lt.size(adjs)):
            adj = lt.get_element(adjs, i)
            if is_in_list(visited, adj):
                continue
            info = G.get_vertex_information(graph, adj)
            if info and mp.contains(info, "domiciliarios"):
                doms = mp.get(info, "domiciliarios")["value"]
                if is_in_list(doms, domiciliario):
                    if not mp.contains(dist, adj) or current_dist + 1 < mp.get(dist, adj)["value"]:
                        mp.put(dist, adj, current_dist + 1)
                        mp.put(parent, adj, current)
                        pq.insert(heap, adj, current_dist + 1)

    end_time = get_time()

    if not found:
        return {"existe": False, "tiempo": delta_time(start_time, end_time)}

    # reconstruir camino
    path = lt.new_list()
    node = destino
    while node != origen:
        lt.add_first(path, node)
        node = mp.get(parent, node)["value"]
    lt.add_first(path, origen)

    # Recopilar domiciliarios únicos y restaurantes
    domiciliarios = lt.new_list()
    restaurantes = lt.new_list()
    for i in range(lt.size(path)):
        nodo = lt.get_element(path, i)
        info = G.get_vertex_information(graph, nodo)
        if info and mp.contains(info, "domiciliarios"):
            doms = mp.get(info, "domiciliarios")["value"]
            for j in range(lt.size(doms)):
                dom = lt.get_element(doms, j)
                add_if_not_present(domiciliarios, dom)
        if info and mp.contains(info, "tipo"):
            tipo = mp.get(info, "tipo")["value"]
            if tipo == "restaurante":
                add_if_not_present(restaurantes, nodo)

    return {
        "existe": True,
        "tiempo": delta_time(start_time, end_time),
        "num_puntos": lt.size(path),
        "camino": path,
        "domiciliarios": domiciliarios,
        "restaurantes": restaurantes
    }


    
def req_3(catalog, punto_geo):
    """
    Retorna el domiciliario con más pedidos en una ubicación geográfica específica
    """
    start = get_time()
    graph = catalog["graph"]
    vertex = G.get_vertex(graph, punto_geo)
    if vertex is None:
        return None

    info = vtx.get_value(vertex)
    if info is None or not mp.contains(info, "domiciliarios"):
        return None

    doms = mp.get(info, "domiciliarios")["value"]
    contador = mp.newMap(100, 0.5)
    max_domiciliario = None
    max_pedidos = 0

    for i in range(lt.size(doms)):
        dom = lt.get_element(doms, i)
        if mp.contains(contador, dom):
            count = mp.get(contador, dom)["value"] + 1
        else:
            count = 1
        mp.put(contador, dom, count)
        if count > max_pedidos:
            max_pedidos = count
            max_domiciliario = dom

    end = get_time()
    return {
        "domiciliario": max_domiciliario,
        "pedidos": max_pedidos,
        "tiempo": delta_time(start, end)
    }


def req_4(catalog, punto_A, punto_B):
    """
    Retorna los domiciliarios en común entre las ubicaciones geográficas A y B
    """
    start = get_time()
    graph = catalog["graph"]
    dom_comunes = lt.new_list()

    vertex_A = G.get_vertex(graph, punto_A)
    vertex_B = G.get_vertex(graph, punto_B)

    if vertex_A is None or vertex_B is None:
        return None

    info_A = vtx.get_value(vertex_A)
    info_B = vtx.get_value(vertex_B)

    doms_A = mp.get(info_A, "domiciliarios")["value"] if mp.contains(info_A, "domiciliarios") else lt.new_list()
    doms_B = mp.get(info_B, "domiciliarios")["value"] if mp.contains(info_B, "domiciliarios") else lt.new_list()

    for i in range(lt.size(doms_A)):
        dom = lt.get_element(doms_A, i)
        if is_in_list(doms_B, dom):
            lt.add_last(dom_comunes, dom)

    end = get_time()
    return {
        "domiciliarios_en_comun": dom_comunes,
        "cantidad": lt.size(dom_comunes),
        "tiempo": delta_time(start, end)
    }


def req_5(catalog, punto_A, N):


    start = get_time()
    graph = catalog["graph"]
    vertex = G.get_vertex(graph, punto_A)
    if vertex is None:
        return None

    info = vtx.get_value(vertex)
    if info is None or not mp.contains(info, "domiciliarios"):
        return None

    doms = mp.get(info, "domiciliarios")["value"]
    mejor_camino = lt.new_list()
    mejor_domiciliario = None
    max_distancia = 0

    for i in range(lt.size(doms)):
        dom_id = lt.get_element(doms, i)
        camino_actual = lt.new_list()
        visitados = mp.newMap(100, 0.5)

        def dfs(actual, profundidad, distancia_acumulada):
            nonlocal mejor_camino, mejor_domiciliario, max_distancia

            lt.add_last(camino_actual, actual)
            mp.put(visitados, actual, True)

            if profundidad == N:
                if distancia_acumulada > max_distancia:
                    max_distancia = distancia_acumulada
                    mejor_domiciliario = dom_id
                    mejor_camino = lt.sub_list(camino_actual, 0, lt.size(camino_actual)-1)
                lt.remove_last(camino_actual)
                mp.remove(visitados, actual)
                return

            adjs = G.adjacents(graph, actual)
            for j in range(lt.size(adjs)):
                vecino = lt.get_element(adjs, j)
                if mp.contains(visitados, vecino):
                    continue
                info_v = G.get_vertex_information(graph, vecino)
                if info_v and mp.contains(info_v, "domiciliarios"):
                    doms_v = mp.get(info_v, "domiciliarios")["value"]
                    if is_in_list(doms_v, dom_id):
                        nueva_distancia = distance_km(actual, vecino)
                        dfs(vecino, profundidad + 1, distancia_acumulada + nueva_distancia)

            lt.remove_last(camino_actual)
            mp.remove(visitados, actual)

        dfs(punto_A, 0, 0)

    end = get_time()
    return {
        "tiempo": delta_time(start, end),
        "domiciliario": mejor_domiciliario,
        "distancia_km": round(max_distancia, 2),
        "camino": mejor_camino
    }



def req_6(catalog, punto_A):



    start = get_time()
    graph = catalog["graph"]
    dist = mp.newMap(500, 0.5)
    parent = mp.newMap(500, 0.5)
    heap = pq.new_heap(is_min_pq=True)
    visited = lt.new_list()

    mp.put(dist, punto_A, 0)
    pq.insert(heap, punto_A, 0)

    while not pq.is_empty(heap):
        current = pq.remove(heap)[1]
        if is_in_list(visited, current):
            continue
        add_if_not_present(visited, current)

        adjs = G.adjacents(graph, current)
        for i in range(lt.size(adjs)):
            neighbor = lt.get_element(adjs, i)
            edge = G.get_edge(graph, current, neighbor)
            if edge is None:
                continue
            weight = edge["weight"]
            current_dist = mp.get(dist, current)["value"]
            new_dist = current_dist + weight

            if not mp.contains(dist, neighbor) or new_dist < mp.get(dist, neighbor)["value"]:
                mp.put(dist, neighbor, new_dist)
                mp.put(parent, neighbor, current)
                pq.insert(heap, neighbor, new_dist)

    # recolectar ubicaciones alcanzables
    ubicaciones = mp.key_set(dist)
    ubicaciones.sort()
    cantidad = len(ubicaciones)

    # encontrar el nodo más costoso (en tiempo)
    max_tiempo = -1
    max_dest = None
    for ub in ubicaciones:
        tiempo = mp.get(dist, ub)["value"]
        if tiempo > max_tiempo:
            max_tiempo = tiempo
            max_dest = ub

    # reconstruir el camino al más costoso
    camino = lt.new_list()
    node = max_dest
    while node != punto_A:
        lt.add_first(camino, node)
        node = mp.get(parent, node)["value"]
    lt.add_first(camino, punto_A)

    end = get_time()
    return {
        "tiempo": delta_time(start, end),
        "cantidad_ubicaciones": cantidad,
        "ubicaciones_ordenadas": ubicaciones,
        "camino_mas_costoso": camino,
        "tiempo_mas_costoso": round(max_tiempo, 2)
    }



def req_7(catalog, punto_A, domiciliario_id):


    start = get_time()
    graph = catalog["graph"]
    visited = mp.newMap(500, 0.5)
    dist = mp.newMap(500, 0.5)
    heap = pq.new_heap(is_min_pq=True)
    total_cost = 0
    ubicaciones = lt.new_list()

    mp.put(dist, punto_A, 0)
    pq.insert(heap, punto_A, 0)

    while not pq.is_empty(heap):
        current = pq.remove(heap)[1]

        if mp.contains(visited, current):
            continue
        mp.put(visited, current, True)
        add_if_not_present(ubicaciones, current)

        if mp.contains(dist, current):
            total_cost += mp.get(dist, current)["value"]

        adjs = G.adjacents(graph, current)
        for i in range(lt.size(adjs)):
            neighbor = lt.get_element(adjs, i)
            if mp.contains(visited, neighbor):
                continue

            info = G.get_vertex_information(graph, neighbor)
            if not info or not mp.contains(info, "domiciliarios"):
                continue

            doms = mp.get(info, "domiciliarios")["value"]
            if not is_in_list(doms, domiciliario_id):
                continue

            edge = G.get_edge(graph, current, neighbor)
            if edge:
                weight = edge["weight"]
                if not mp.contains(dist, neighbor) or weight < mp.get(dist, neighbor)["value"]:
                    mp.put(dist, neighbor, weight)
                    pq.insert(heap, neighbor, weight)

    end = get_time()
    ubicaciones_ordenadas = [lt.get_element(ubicaciones, i) for i in range(lt.size(ubicaciones))]
    ubicaciones_ordenadas.sort()

    return {
        "tiempo": delta_time(start, end),
        "cantidad_ubicaciones": lt.size(ubicaciones),
        "ubicaciones": ubicaciones_ordenadas,
        "costo_total": round(total_cost, 2)
    }


def req_8(catalog):
    pass

# Funciones para medir tiempos de ejecucion

def get_time():
    return float(time.perf_counter() * 1000)

def delta_time(start, end):
    return float(end - start)



def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radio Tierra en km
    lat1, lon1, lat2, lon2 = map(radians, [float(lat1), float(lon1), float(lat2), float(lon2)])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def distance_km(coord1, coord2):
    lat1, lon1 = map(float, coord1.split("_"))
    lat2, lon2 = map(float, coord2.split("_"))
    return haversine(lat1, lon1, lat2, lon2)
