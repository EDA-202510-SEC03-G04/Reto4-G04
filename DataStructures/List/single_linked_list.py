

def new_list():
    newlist = {
        "first": None,
        "last": None,
        "size": 0,
    }
    return newlist

def get_element(my_list, pos):
    searchpos = 0 
    node = my_list["first"]
    while searchpos < pos:
        node = node["next"]
        searchpos +=1
    return node["info"]


def is_present(my_list, element, cmp_function):
    is_in_array = False
    temp = my_list["first"]
    count = 0 
    while not is_in_array and temp is not None:
        if cmp_function(element, temp["info"]) == 0:
            is_in_array = True
        else: 
            temp = temp["next"]
            count += 1 
            
    if not is_in_array:
        count = -1
    return count

def add_first(my_list, element):

    new_node = {
        "info": element,
        "next": my_list["first"]  
    }
    
    my_list["first"] = new_node
  
    if my_list["size"] == 0:
        my_list["last"] = new_node

    my_list["size"] += 1

def add_last(my_list, element):

    new_node = { 
        "info": element, 
        "next": None
    }
    
    if my_list["size"] == 0: 
        my_list["first"] = new_node
        my_list["last"] = new_node
        
    else: 
        
        my_list["last"]["next"] = new_node
        my_list["last"] = new_node
        
    my_list["size"] += 1  #No se les olvide siempre actualizar el tamaño
    

def is_empty(my_list):

    if my_list["size"] > 0: 
        return False
    else:
        return True
    
def size(my_list):
    
    return my_list["size"]

def first_element(my_list):
    
    if is_empty(my_list):
        raise Exception('IndexError: list index out of range')
    
    else: 
        return my_list["first"]
    
    
def last_element(my_list):
    
    if is_empty(my_list):
        raise Exception('IndexError: list index out of range')
    
    else:
        return my_list["last"]
    
    
def remove_first(my_list):
    if my_list["size"] == 0:
        raise Exception('IndexError: list index out of range')
    
    eliminado = my_list["first"]["info"]
    
    my_list["first"] = my_list["first"]["next"]
    
    if my_list["first"] is None: 
        my_list["last"] = None 
        
        
    my_list["size"] -= 1 #Actualizar tamaño
    
    return eliminado
        
        
def remove_last(my_list):
    
    if my_list["size"] == 1:
        
        eliminado = my_list["last"]["info"]
        
        my_list["first"] = None
        my_list["last"] = None
        my_list["size"] -= 1 
        return eliminado
        
    actual = my_list["first"]
    
    while actual["next"] != my_list["last"]:
        actual = actual["next"]

    eliminado = my_list["last"]["info"]
    
    actual["next"] = None
    my_list["last"] = actual
    
    my_list["sizw"] -= 1 
    
    return eliminado   


def insert_element(my_list, element, pos):
    
    if pos < 0 or pos > size(my_list):  
        raise Exception('IndexError: list index out of range')
    
    if pos == 0:
        
        add_first(my_list, element)
        return my_list
    
    if pos == my_list["size"]:
        
        add_last(my_list, element)
        return my_list
    
    nuevo_nodo = {"info": element, "next": None}
    
    curr = my_list["first"]
    for _ in range(pos - 1):
        curr = curr["next"]
        
    nuevo_nodo["next"] = curr["next"]
    
    curr["next"] = nuevo_nodo
    
    my_list["size"] += 1 
    
    return my_list
    
    
def delete_element(my_list, pos):
    
    if pos < 0 or pos >= my_list["size"]:
        raise IndexError("Posición fuera de rango")
    
    if pos == 0:
        return remove_first(my_list)

    
    if pos == my_list["size"] - 1:
        return remove_last(my_list)
    
    current = my_list["first"]
    
    for _ in range(pos - 1):
        current = current["next"]
        
    removed_value = current["next"]["info"]
    
    current["next"] = current["next"]["next"]
    
    my_list["size"] -= 1

    return removed_value

def change_info(my_list, pos, new_info):
    
    if pos < 0 or pos >= my_list["size"]:  # Posición fuera de rango
        raise IndexError("Posición fuera de rango")
    
    current = my_list["first"]
    for _ in range(pos):
        current = current["next"]
        
    current["info"] = new_info
    
    return my_list

def exchange(my_list, pos_1, pos_2):
    if pos_1 < 0 or pos_1 >= my_list["size"] or pos_2 < 0 or pos_2 >= my_list["size"]:
        raise IndexError("Una de las posiciones está fuera de rango")

    if pos_1 == pos_2:  # No hay nada que intercambiar
        return my_list

    
    current_1 = my_list["first"]
    for _ in range(pos_1):
        current_1 = current_1["next"]

    current_2 = my_list["first"]
    for _ in range(pos_2):
        current_2 = current_2["next"]

    
    current_1["info"], current_2["info"] = current_2["info"], current_1["info"]

    return my_list  


def sub_list(my_list, start, end):
    if start < 0 or start >= my_list["size"] or end <= start:
        return {"first": None, "last": None, "size": 0}  # Retorna lista vacía

    if end > my_list["size"]:
        end = my_list["size"]  

    sublist = {"first": None, "last": None, "size": 0}
    current = my_list["first"]
    

    for _ in range(start):
        current = current["next"]

    
    while start < end:
        new_node = {"info": current["info"], "next": None}

        if sublist["first"] is None:
            sublist["first"] = new_node
            sublist["last"] = new_node
        else:
            sublist["last"]["next"] = new_node
            sublist["last"] = new_node
        
        current = current["next"]
        start += 1
        sublist["size"] += 1

    return sublist  # Retornar la sublista generada


    
    