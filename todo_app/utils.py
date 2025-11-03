def mostrar_tareas(lista):
    if not lista:
        print("No hay tareas para mostrar.")
        return

    for t in lista:
        estado = "Completada" if t["completada"] else "Pendiente"
        print(f"""
   ID: {t["id"]}
   Descripción: {t["descripcion"]}
   Prioridad: {t["prioridad"].capitalize()}
   Categoría: {t["categoria"]["principal"]} / {t["categoria"]["sub"]}
   Estado: {estado}
        """)

def mostrarMenu(menu = 0):
    match menu:
        case 0:
            print(" MENÚ DE OPCIONES")
            print(" 0 - Salir de la aplicacion") #añadir un desea salir sin guardar?
            print(" 1 - Cargar tareas")
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
            print("     5 - Buscar una tarea")
            print("     6 - Marcar como completada")
        case 3:
            print("         0 - Volver")
            print("         1 - Listar todas las tareas")
            print("         2 - Listar tareas completadas")
            print("         3 - Listar tareas pendientes")
        case 4:
            print("         0 - Volver")
            print("         1 - Buscar por categoría")
            print("         2 - Buscar por palabra clave")


def buscar_categoria_recursiva(estructura, categoria, contexto=None):
    """
    Busca recursivamente 'categoria' dentro de 'estructura'.
    Devuelve SIEMPRE una lista de tareas (diccionarios completos) que coinciden.
    'contexto' es el diccionario de la tarea actual (si se está procesando una tarea).
    """
    resultados = []

    # Si es una lista, llamamos recursivamente sobre cada elemento (manteniendo contexto)
    if isinstance(estructura, list):
        if not estructura:
            return []
        # primera posición + resto (recursivo)
        return (buscar_categoria_recursiva(estructura[0], categoria, contexto)
                + buscar_categoria_recursiva(estructura[1:], categoria, contexto))

    # Si es un diccionario
    if isinstance(estructura, dict):
        # Si este diccionario parece una tarea (tiene 'id' o 'descripcion'), lo tomamos como nuevo contexto
        if 'id' in estructura:
            contexto = estructura

        # Recorremos sus valores y llamamos recursivamente
        for valor in estructura.values():
            # Si el valor es otra estructura, buscamos dentro (pasando el contexto actual)
            if isinstance(valor, (list, dict)):
                resultados += buscar_categoria_recursiva(valor, categoria, contexto)
            else:
                # Si el valor es un valor simple y coincide con la categoría buscada
                if valor == categoria and contexto is not None:
                    # añadimos la tarea completa (contexto) si aún no está añadida
                    if contexto not in resultados:
                        resultados.append(contexto)

        return resultados

    # Si es cualquier otro tipo (p. ej. str, int) y no un dict/list, no hay coincidencia
    return []