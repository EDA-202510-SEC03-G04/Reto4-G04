def new_list():
    newlist = {
        'elements' : [],
        'size' : 0,    
    }
    return newlist

def get_element(my_list,index):
    
    return my_list["elements"][index]

def is_present(my_list,element, cmp_function):
    
    size = my_list["size"]
    if size > 0:
        keyexist = False
        for keypos in range(0,size):
            info = my_list["elements"][keypos]
            if cmp_function(element, info) == 0: 
                keyexist = True
                break
        if keyexist:
            return keypos
    return -1

def cmp_function(element1, element2):
    if element1 > element2:
        return 1
    elif element1 < element2:
        return -1
    else:
        return 0
  


def add_first(my_list, element):
    my_list["elements"].insert(0, element)
    my_list["size"] += 1
    return my_list

def add_last(my_list, element):
    my_list["elements"].append(element)
    my_list["size"] += 1
    return my_list

   
def is_empty(my_list):

    if my_list["size"] < 1:
        return True
    else:
        return False
    
def size(my_list):

    return my_list["size"]
    
def first_element(my_list):
    
    return my_list["elements"][0]
    
    
def last_element(my_list):
    
    return my_list["elements"][-1]

def remove_first(my_list):
    
    if my_list["size"] > 0:  
        eliminado = my_list["elements"].pop(0)  # Elimina el primer elemento
        my_list["size"] -= 1
        return eliminado 
    else: 
        return None

def remove_last(my_list):
    
    if my_list["size"] > 0:  
        eliminado = my_list["elements"].pop(-1)  
        my_list["size"] -= 1
        return eliminado 
    else:
        return None
    
def insert_element(my_list, element, pos):
    
    if pos < 0 or pos > my_list["size"]:  # Toca verificar si la posición es válida
        raise IndexError("Posición fuera de rango")  
    
    my_list["elements"].insert(pos, element)  
    my_list["size"] += 1  
    
    return my_list

def delete_element(my_list, pos):
    
    if pos < 0 or pos >= my_list["size"]:  # Toca verificar si la posición es válida
        raise IndexError("Posición fuera de rango")  
    
    my_list["elements"].pop(pos)  
    my_list["size"] -= 1  
    
    return my_list

def change_info(my_list, pos, new_info):
    
    if pos < 0 or pos >= my_list["size"]:  
        raise IndexError("Posición fuera de rango") 
    
    my_list["elements"][pos] = new_info
    
    return my_list 

def exchange(my_list, pos_1, pos_2):
    
    if pos_1 < 0 or pos_1 >= my_list["size"] or pos_2 < 0 or pos_2 >= my_list["size"]:
        raise IndexError("Una de las posiciones está fuera de rango")  
    
    cebo = my_list["elements"][pos_1]
    
    my_list["elements"][pos_1] = my_list["elements"][pos_2]
    my_list["elements"][pos_2] = cebo
    
    return my_list

def sub_list(my_list, pos_i, num_elements):
    
    sublist = {
        "size": num_elements - pos_i + 1,
        "elements": my_list["elements"][pos_i:num_elements + 1]  # acá saca una sublista
    }
    
    return sublist

