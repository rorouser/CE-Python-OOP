from entities import *

def buscar_tareas(tareas, id):
    return [t for t in tareas if t.id == int(id)][0]

def mostrar_tareas(lista):
    if not lista:
        print("No hay tareas para mostrar.")
        return

    for t in lista:
        print(t)

def get_info():
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
            print(" --info")
        case 2:
            print("     0 - Salir al menú principal")
            print("     1 - Listar tareas")
            print("     2 - Agregar una tarea")
            print("     3 - Editar una tarea")
            print("     4 - Eliminar una tarea")
            print("     5 - Buscar tareas por palabra clave")
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

def generar_informe_estadisticas(tareas):
    """
    Genera informe de estadisticas en la aplicacion sobre si las tareas están completadas, pendientes y el porcentaje de las tareas completas.
    """
    if not tareas:
        return "No hay tareas cargadas para generar estadísticas.\n"

    total = len(tareas)
    completadas = sum(t.completada for t in tareas)
    pendientes = total - completadas
    porcentaje = (completadas / total * 100) if total else 0

    prioridades = {p: sum(1 for t in tareas if t.prioridad.value == p)  for p in {t.prioridad.value for t in tareas}}

    categorias = {c: sum(1 for t in tareas if t.categoria.principal.value == c) for c in {t.categoria.principal.value for t in tareas}}

    subcategorias = {s: sum(1 for t in tareas if t.categoria.sub and t.categoria.sub.value == s) for s in {t.categoria.sub.value for t in tareas if t.categoria.sub}}

    informe = [
        "=== INFORME DE ESTADÍSTICAS ===\n",
        f"Total de tareas: {total}",
        f"Tareas completadas: {completadas}",
        f"Tareas pendientes: {pendientes}",
        f"Porcentaje completadas: {porcentaje:.2f}%\n",
        "=== Por prioridad ===",
        *[f"  {p.capitalize()}: {i}" for p, i in prioridades.items()],
        "\n=== Por categoría ===",
        *[f"  {c}: {i}" for c, i in categorias.items()],
        "\n=== Por subcategoría ===",
        *[f"  {s}: {i}" for s, i in subcategorias.items()],
        ""
    ]

    return "\n".join(informe)


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