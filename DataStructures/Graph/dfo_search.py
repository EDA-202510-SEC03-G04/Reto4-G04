from DataStructures.Queue import queue
from DataStructures.Stack import stack

def new_dfo_search():
    """
    Crea una estructura de busqueda usada en el algoritmo **depth_first_order**.

    Se crea una estructura de busqueda con los siguientes atributos:

    - **marked**: Mapa con los vertices visitados. Se inicializa en ``None``
    - **pre**: Cola con los vertices visitados en preorden. Se inicializa como una cola vacia.
    - **post**: Cola con los vertices visitados en postorden. Se inicializa como una cola vacia.
    - **reversepost**: Pila con los vertices visitados en postorden inverso. Se inicializa como una pila vacia.

    :returns: Estructura de busqueda
    :rtype: dfo_search
    """
    search = {
        'marked': None,
        'pre': queue.new_queue(),
        'post': queue.new_queue(),
        'reversepost': stack.new_stack()
    }
    return search