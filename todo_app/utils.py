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
            print("             5 - Guardar")


def buscar_por_categoria(estructura, categoria, tarea=None):
    """
    Busca recursivamente 'categoria' dentro de 'estructura'.
    Devuelve SIEMPRE una lista de tareas (diccionarios completos) que coinciden.
    'tarea' es el diccionario de la tarea actual (si se está procesando una tarea).
    """
    resultados = []

    # Si es una lista, llamamos recursivamente sobre cada elemento (manteniendo tarea)
    if isinstance(estructura, list):
        if not estructura:
            return []
        # primera posición + resto (recursivo)
        return (buscar_por_categoria(estructura[0], categoria, tarea)
                + buscar_por_categoria(estructura[1:], categoria, tarea))

    # Si es un diccionario
    if isinstance(estructura, dict):
        # Si este diccionario parece una tarea (tiene 'id' o 'descripcion'), lo tomamos como nuevo tarea
        if 'id' in estructura:
            tarea = estructura

        # Recorremos sus valores y llamamos recursivamente
        for valor in estructura.values():
            # Si el valor es otra estructura, buscamos dentro (pasando el tarea actual)
            if isinstance(valor, (list, dict)):
                resultados += buscar_por_categoria(valor, categoria, tarea)
            else:
                # Si el valor es un valor simple y coincide con la categoría buscada
                if valor == categoria and tarea is not None:
                    # añadimos la tarea completa (contexto) si aún no está añadida
                    if tarea not in resultados:
                        resultados.append(tarea)

        return resultados

    # Si es cualquier otro tipo (p. ej. str, int) y no un dict/list, no hay coincidencia
    return []

