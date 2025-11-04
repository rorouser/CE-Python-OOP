from entities import Tarea, Categoria

def buscar_tareas(tareas, id):
    return [t for t in tareas if t.id == int(id)][0]

def mostrar_tareas(lista):
    if not lista:
        print("No hay tareas para mostrar.")
        return

    for t in lista:
        print(t)

def mostrarMenu(menu = 0, tareas_cargadas = True):
    match menu:
        case 0:
            print(" MENÚ DE OPCIONES")
            print(" 0 - Salir de la aplicacion") #añadir un desea salir sin guardar?
            if not tareas_cargadas:
                print(" 1 - Cargar tareas")
            if tareas_cargadas:
                print(" 2 - Tareas")
                print(" 3 - Guardar cambios")
                print(" 4 - Generar informe de estadísticas")
            print(" --help")
        case 2:
            print("     0 - Salir al menú principal")
            print("     1 - Listar tareas")
            print("     2 - Agregar una tarea")
            print("     3 - Editar una tarea")
            print("     4 - Eliminar una tarea")
            print("     5 - Buscar una tarea por categoría o palabra clave")
            print("     6 - Marcar como completada")
        case 3:
            print("         0 - Volver")
            print("         1 - Listar todas las tareas")
            print("         2 - Listar tareas completadas")
            print("         3 - Listar tareas pendientes")
        case 4:
            print("         0 - Volver")
            print("         1 - Listar tareas")
            print("         2 - Editar tarea")
        case 5:
            print("             0 - Volver")
            print("             1 - Editar descripcion")
            print("             2 - Editar prioridad")
            print("             3 - Editar categoria")
            print("             4 - Editar subcategoria")
        case 6:
            print("         0 - Volver")
            print("         1 - Listar tareas pendientes")
            print("         2 - Marcar como completada")


def buscar_por_categoria(estructura, categoria_buscada, tarea=None):
    """
    Busca recursivamente una categoría dentro de una estructura compuesta por objetos Tarea y Categoria.
    Devuelve una lista con las tareas (objetos Tarea) que coinciden con la categoría buscada.
    """
    resultados = []

    # 🧩 Caso 1: si es lista, recorremos cada elemento recursivamente
    if isinstance(estructura, list):
        if not estructura:
            return []
        return (
            buscar_por_categoria(estructura[0], categoria_buscada, tarea)
            + buscar_por_categoria(estructura[1:], categoria_buscada, tarea)
        )

    if isinstance(estructura, Tarea):
        tarea = estructura
        return buscar_por_categoria(estructura.categoria, categoria_buscada, tarea)

    if isinstance(estructura, Categoria):
        # buscamos coincidencias directas
        for campo in ["principal", "sub"]:
            valor = getattr(estructura, campo, None)
            if valor == categoria_buscada and tarea is not None:
                resultados.append(tarea)
        return resultados

    # 🧩 Caso 4: cualquier otro tipo → nada que buscar
    return []