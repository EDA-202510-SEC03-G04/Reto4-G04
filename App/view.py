import sys
from tabulate import tabulate
import App.logic as controller
from DataStructures.List import array_list as lt


def new_logic():
    return controller.new_logic()


def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Ejecutar Requerimiento 1")
    print("3- Ejecutar Requerimiento 2")
    print("4- Ejecutar Requerimiento 3")
    print("5- Ejecutar Requerimiento 4")
    print("6- Ejecutar Requerimiento 5")
    print("7- Ejecutar Requerimiento 6")
    print("8- Ejecutar Requerimiento 7")
    print("9- Ejecutar Requerimiento 8 (Bono)")
    print("0- Salir")


def load_data(control):
    filename = input("Ingrese el nombre del archivo CSV: ")
    filepath = f"data/{filename}"
    resumen = controller.load_data(control, filepath)

    print("\nDatos cargados correctamente.\n")
    print(tabulate([
        ["# Domicilios", resumen["n_domicilios"]],
        ["# Domiciliarios únicos", resumen["n_domiciliarios"]],
        ["# Nodos (ubicaciones)", resumen["n_vertices"]],
        ["# Arcos (conexiones)", resumen["n_aristas"]],
        ["# Restaurantes únicos", resumen["n_restaurantes"]],
        ["# Destinos únicos", resumen["n_destinos"]],
        ["Tiempo promedio de entrega (min)", resumen["tiempo_promedio"]]
    ], headers=["Estadística", "Valor"], tablefmt="fancy_grid"))


def print_list(title, lst):
    print(title)
    for i in range(lt.size(lst)):
        print(f"- {lt.get_element(lst, i)}")


def print_req_1(control):
    origen = input("Ubicación origen (lat_lon): ")
    destino = input("Ubicación destino (lat_lon): ")
    resultado = controller.req_1(control, origen, destino)
    if not resultado["existe"]:
        print("No existe camino entre los puntos.")
    else:
        print(f"\nCamino encontrado en {resultado['tiempo']:.2f} ms")
        print(f"Número de puntos en el camino: {resultado['num_puntos']}")
        print_list("Camino:", resultado["camino"])
        print_list("Domiciliarios en el camino:", resultado["domiciliarios"])
        print_list("Restaurantes en el camino:", resultado["restaurantes"])


def print_req_2(control):
    origen = input("Ubicación origen (lat_lon): ")
    destino = input("Ubicación destino (lat_lon): ")
    domiciliario = input("ID del domiciliario: ")
    resultado = controller.req_2(control, origen, destino, domiciliario)
    if not resultado["existe"]:
        print("No existe camino para ese domiciliario entre los puntos.")
    else:
        print(f"\nCamino encontrado en {resultado['tiempo']:.2f} ms")
        print(f"Número de puntos en el camino: {resultado['num_puntos']}")
        print_list("Camino:", resultado["camino"])
        print_list("Domiciliarios en el camino:", resultado["domiciliarios"])
        print_list("Restaurantes en el camino:", resultado["restaurantes"])


def print_req_3(control):
    punto = input("Ingrese la ubicación geográfica (lat_lon): ")
    resultado = controller.req_3(control, punto)
    if resultado:
        print(tabulate([[resultado['domiciliario'], resultado['pedidos'], f"{resultado['tiempo']:.2f} ms"]],
                       headers=["Domiciliario", "Pedidos", "Tiempo"], tablefmt="fancy_grid"))
    else:
        print("Ubicación no encontrada o sin datos.")


def print_req_4(control):
    punto_A = input("Ubicación A (lat_lon): ")
    punto_B = input("Ubicación B (lat_lon): ")
    resultado = controller.req_4(control, punto_A, punto_B)
    if resultado:
        print(f"Domiciliarios en común entre {punto_A} y {punto_B}: {resultado['cantidad']}")
        print_list("Domiciliarios:", resultado["domiciliarios_en_comun"])
        print(f"Tiempo de ejecución: {resultado['tiempo']:.2f} ms")
    else:
        print("Una o ambas ubicaciones no existen.")


def print_req_5(control):
    punto = input("Ingrese la ubicación geográfica inicial (lat_lon): ")
    n = int(input("Número de cambios de ubicación N: "))
    resultado = controller.req_5(control, punto, n)
    if resultado:
        print(f"\nDomiciliario con mayor recorrido: {resultado['domiciliario']}")
        print(f"Distancia recorrida: {resultado['distancia_km']} km")
        print(f"Tiempo de ejecución: {resultado['tiempo']:.2f} ms")
        print("Camino recorrido:")
        for i in range(lt.size(resultado["camino"])):
            print(" →", lt.get_element(resultado["camino"], i))
    else:
        print("No se encontró un camino válido.")



def print_req_6(control):
    punto = input("Ingrese la ubicación geográfica inicial (lat_lon): ")
    resultado = controller.req_6(control, punto)
    if resultado:
        print(f"\nTiempo total de ejecución: {resultado['tiempo']:.2f} ms")
        print(f"Cantidad de ubicaciones alcanzables: {resultado['cantidad_ubicaciones']}")
        print("Ubicaciones alcanzables:")
        for ub in resultado["ubicaciones_ordenadas"]:
            print("-", ub)
        print("\nCamino más costoso:")
        for i in range(lt.size(resultado["camino_mas_costoso"])):
            print(" →", lt.get_element(resultado["camino_mas_costoso"], i))
        print(f"Tiempo total del camino: {resultado['tiempo_mas_costoso']} min")
    else:
        print("No se encontraron ubicaciones alcanzables.")



def print_req_7(control):
    punto = input("Ingrese la ubicación geográfica inicial (lat_lon): ")
    dom_id = input("Ingrese el ID del domiciliario: ")
    resultado = controller.req_7(control, punto, dom_id)
    if resultado:
        print(f"\nTiempo de ejecución: {resultado['tiempo']:.2f} ms")
        print(f"Cantidad de ubicaciones conectadas: {resultado['cantidad_ubicaciones']}")
        print("Ubicaciones conectadas:")
        for ub in resultado["ubicaciones"]:
            print(" -", ub)
        print(f"Tiempo total del MST: {resultado['costo_total']} min")
    else:
        print("No fue posible construir el árbol de recubrimiento mínimo.")


def print_req_8(control):
    print("Requerimiento 8 no implementado aún.")

# Se crea la lógica asociado a la vista
control = new_logic()

# main del ejercicio
def main():
    working = True
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 1:
            load_data(control)
        elif int(inputs) == 2:
            print_req_1(control)
        elif int(inputs) == 3:
            print_req_2(control)
        elif int(inputs) == 4:
            print_req_3(control)
        elif int(inputs) == 5:
            print_req_4(control)
        elif int(inputs) == 6:
            print_req_5(control)
        elif int(inputs) == 7:
            print_req_6(control)
        elif int(inputs) == 8:
            print_req_7(control)
        elif int(inputs) == 9:
            print_req_8(control)
        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)


if __name__ == "__main__":
    main()
