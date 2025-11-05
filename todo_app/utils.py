from entities import *

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
    Busca recursivamente tareas que coincidan con una prioridad, categoría principal o subcategoría.
    El parámetro `categoria_buscada` puede ser un string o un Enum.
    Devuelve una lista con las tareas que cumplan el criterio.
    """
    resultados = []

    # 🧩 Caso 1: si es lista → recorrer recursivamente
    if isinstance(estructura, list):
        if not estructura:
            return []
        return (
            buscar_por_categoria(estructura[0], categoria_buscada, tarea)
            + buscar_por_categoria(estructura[1:], categoria_buscada, tarea)
        )

    # 🧩 Caso 2: si es una tarea
    if isinstance(estructura, Tarea):
        tarea = estructura

        # --- Normalizamos la búsqueda si es string ---
        busqueda = categoria_buscada.strip().lower() if isinstance(categoria_buscada, str) else categoria_buscada

        # --- Buscar coincidencia por prioridad ---
        if (
            (isinstance(busqueda, Prioridad) and tarea.prioridad == busqueda)
            or (isinstance(busqueda, str) and tarea.prioridad.value == busqueda)
        ):
            resultados.append(tarea)

        # --- Buscar en la categoría ---
        resultados += buscar_por_categoria(estructura.categoria, categoria_buscada, tarea)
        return resultados

    # 🧩 Caso 3: si es una categoría
    if isinstance(estructura, Categoria):
        cat = estructura
        busqueda = categoria_buscada.strip().lower() if isinstance(categoria_buscada, str) else categoria_buscada

        # --- Si la búsqueda es un Enum de categoría principal ---
        if isinstance(busqueda, CategoriaPrincipal) and cat.principal == busqueda:
            resultados.append(tarea)

        # --- Si es un Enum de subcategoría ---
        elif any(isinstance(busqueda, sub_enum) for sub_enum in SUBCATEGORIAS_POR_CATEGORIA.values()):
            if cat.sub == busqueda:
                resultados.append(tarea)

        # --- Si es texto: comparar con nombres de categoría o subcategoría ---
        elif isinstance(busqueda, str):
            if (
                cat.principal.value.lower() == busqueda
                or cat.sub.value.lower() == busqueda
            ):
                resultados.append(tarea)

        return resultados

    # 🧩 Caso 4: otro tipo → nada que buscar
    return []

