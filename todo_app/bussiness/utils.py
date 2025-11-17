from todo_app.data.entities import *

def buscar_tareas(tareas, id):
    '''Busca y devuelve la tarea con el id indicado de la lista dada.'''
    return [t for t in tareas if t.id == int(id)][0]

def mostrar_tareas(lista):
    '''Muestra por pantalla las tareas de la lista dada.'''
    if not lista:
        print("No hay tareas para mostrar.")
        return

    for t in lista:
        print(t)

def crear_tarea(tareas, descripcion, prioridad, categoria, subcategoria):
    '''Crea y devuelve la tarea'''
    return Tarea(
                id = max([t.id for t in tareas], default=0) + 1,
                descripcion = descripcion,
                prioridad = prioridad,
                completada = False,
                categoria = Categoria(principal = categoria,
                                      sub = subcategoria))

def get_info():
    ''''Devuelve la información del sistema como una cadena de texto.'''
    return """
    === INFO DEL SISTEMA ===

    Esta aplicación permite gestionar una lista de tareas personales.
    Incluye funciones para:

    • Cargar y guardar tareas desde archivo
    • Listar todas las tareas o filtrarlas por estado
    • Agregar nuevas tareas con descripción, prioridad y categorías
    • Editar tareas existentes
    • Eliminar tareas
    • Buscar tareas por palabra clave
    • Marcar tareas como completadas
    • Generar un informe de estadísticas sobre el estado de las tareas

    Navega por los menús introduciendo el número correspondiente.
    Escribe '--info' en cualquier momento para volver a ver esta información.
    """

def mostrarMenu(menu = 0, tareas_cargadas = True):
    '''Muestra el menú de opciones según el nivel indicado.'''
    match menu:
        case 0:
            print("\n=== TASKMASTER CLI ===\n",)
            print(" MENÚ DE OPCIONES")
            print(" 0 - Salir de la aplicacion") #añadir un desea salir sin guardar?
            if not tareas_cargadas:
                print(" 1 - Cargar tareas")
            if tareas_cargadas:
                print(" 2 - Tareas")
                print(" 3 - Guardar cambios")
                print(" 4 - Generar informe de estadísticas")
            print(" --info\n")
        case 2:
            print("\n     0 - Salir al menú principal")
            print("     1 - Listar tareas")
            print("     2 - Agregar una tarea")
            print("     3 - Editar una tarea")
            print("     4 - Eliminar una tarea")
            print("     5 - Buscar tareas por palabra clave")
            print("     6 - Marcar como completada\n")
        case 3:
            print("\n         0 - Volver")
            print("         1 - Listar todas las tareas")
            print("         2 - Listar tareas completadas")
            print("         3 - Listar tareas pendientes\n")
        case 4:
            print("\n         0 - Volver")
            print("         1 - Listar tareas")
            print("         2 - Editar tarea\n")
        case 5:
            print("\n             0 - Volver")
            print("             1 - Editar descripcion")
            print("             2 - Editar prioridad")
            print("             3 - Editar categoria")
            print("             4 - Editar subcategoria\n")
        case 6:
            print("\n         0 - Volver")
            print("         1 - Listar tareas pendientes")
            print("         2 - Marcar como completada\n")


def pedir_prioridad():
    """Pide al usuario que elija una prioridad válida."""
    opciones = [p.value for p in Prioridad]
    print(f"Opciones de prioridad: {', '.join(o.capitalize() for o in opciones)}")

    # Pedir al usuario hasta que elija una válida
    while True:
        entrada = input("Prioridad: ").strip().capitalize()
        if entrada in opciones:
            return Prioridad(entrada)
        print("Opción no válida. Intenta de nuevo.")

def pedir_categoria():
    """Pide al usuario que elija una categoría principal válida."""
    opciones = [c.value for c in CategoriaPrincipal]
    print(f"Opciones de categoría: {', '.join(opciones)}")

    while True:
        entrada = input("Categoría: ").strip().capitalize()
        for cat in CategoriaPrincipal:
            if cat.value.lower() == entrada.lower():
                return cat
        print("Categoría no válida. Intenta de nuevo.")


def pedir_subcategoria(categoria_principal):
    '''
    Pide una subcategoría válida según la categoría principal seleccionada.
    Recibe un valor de CategoriaPrincipal.
    '''
    sub_enum_cls = SUBCATEGORIAS_POR_CATEGORIA.get(categoria_principal)
    if not sub_enum_cls:
        print(f"No hay subcategorías definidas para {categoria_principal.value}.")
        return None

    opciones = [s.value for s in sub_enum_cls]
    print(f"Opciones de subcategoría para {categoria_principal.value}: {', '.join(opciones)}")

    while True:
        entrada = input("Subcategoría: ").strip().capitalize()
        for sub in sub_enum_cls:
            if sub.value.lower() == entrada.lower():
                return sub
        print("Subcategoría no válida. Intenta de nuevo.")

def buscar_por_palabra_clave(estructura, categoria_buscada, tarea=None):
    """
    Busca recursivamente tareas que coincidan con una prioridad, categoría principal,
    subcategoría o palabras sueltas dentro de la descripción.
    El parámetro `categoria_buscada` puede ser un string o un Enum.
    Devuelve una lista con las tareas que cumplan el criterio.
    """
    resultados = []

    if isinstance(estructura, list):
        if not estructura:
            return []
        return (
            buscar_por_palabra_clave(estructura[0], categoria_buscada, tarea)
            + buscar_por_palabra_clave(estructura[1:], categoria_buscada, tarea)
        )

    if isinstance(estructura, Tarea):
        tarea = estructura
        busqueda = categoria_buscada.strip().lower() if isinstance(categoria_buscada, str) else categoria_buscada

        if (
            (isinstance(busqueda, Prioridad) and tarea.prioridad == busqueda)
            or (isinstance(busqueda, str) and busqueda in tarea.prioridad.value.lower())
        ):
            resultados.append(tarea)

        if isinstance(busqueda, str) and busqueda in tarea.descripcion.lower():
            resultados.append(tarea)

        resultados += buscar_por_palabra_clave(estructura.categoria, categoria_buscada, tarea)
        return resultados

    if isinstance(estructura, Categoria):
        cat = estructura
        busqueda = categoria_buscada.strip().lower() if isinstance(categoria_buscada, str) else categoria_buscada

        if isinstance(busqueda, CategoriaPrincipal) and cat.principal == busqueda:
            resultados.append(tarea)

        elif any(isinstance(busqueda, sub_enum) for sub_enum in SUBCATEGORIAS_POR_CATEGORIA.values()):
            if cat.sub == busqueda:
                resultados.append(tarea)

        elif isinstance(busqueda, str):
            if (
                busqueda in cat.principal.value.lower()
                or busqueda in cat.sub.value.lower()
            ):
                resultados.append(tarea)

        return resultados

    return []