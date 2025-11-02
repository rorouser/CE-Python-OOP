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

