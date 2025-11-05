import utils
import data_handler
from entities import *

# Función del programa principal
def main():
    continuar = True
    tareas = []
    tareas_cargadas = False
    guardado = True
    while continuar:
        utils.mostrarMenu(tareas_cargadas=tareas_cargadas)
        opcion = input("Seleccione una opción: ")
        match opcion:
            case "0":
                # 0 - Salir de la aplicacion
                if not guardado:
                    salir = True
                    while salir:
                        opcion_guardado = input("¿Seguro que quiere salir sin guardar? S/N: ")
                        match opcion_guardado.upper():
                            case "S":
                                continuar = False
                                salir = False
                            case "N":
                                salir = False
                            case _:
                                print("Opción no válida, intenta de nuevo.")
                else:
                    continuar = False

            case "1":
                # 1 - Cargar tareas
                try:
                    tareas = data_handler.cargar_lista_json()
                    print("Tareas cargadas correctamente")
                    tareas_cargadas = True

                except FileNotFoundError as e:
                    print(f"No se pudo cargar la lista: {e}")

                except ValueError as e:
                    print(f"Error en el formato del archivo: {e}")

                except Exception as e:
                    print(f"Error inesperado: {e}")

            case "2":
                # 2 - Tareas
                if tareas_cargadas:
                    continuar_submenu = True
                    while continuar_submenu:
                        utils.mostrarMenu(2)
                        opcion_submenu = input("Seleccione una opción: ")
                        match opcion_submenu:
                            case "0":
                                # 0 - Salir al menú principal
                                continuar_submenu = False

                            case "1":
                                # 1 - Listar tareas
                                try:
                                    continuar_submenu_tareas = True
                                    while continuar_submenu_tareas:
                                        utils.mostrarMenu(3)
                                        opcion_listar_tareas = input("Seleccione una opción: ")
                                        match opcion_listar_tareas:
                                            case "0":
                                                # 0 - Volver
                                                continuar_submenu_tareas = False

                                            case "1":
                                                # 1 - Listar todas las tareas
                                                utils.mostrar_tareas(tareas)

                                            case "2":
                                                # 2 - Listar tareas completadas
                                                utils.mostrar_tareas([t for t in tareas if t.completada])

                                            case "3":
                                                # 3 - Listar tareas pendientes
                                                utils.mostrar_tareas([t for t in tareas if not t.completada])

                                            case _:
                                                print("Opción no válida, intenta de nuevo.")

                                except Exception as e:
                                    print(f"Error al recuperar documentos: {e}")

                            case "2":
                                # 2 - Agregar una tarea
                                try:
                                    descripcion = input("Descripción: ")
                                    prioridad = pedir_prioridad()
                                    categoria = pedir_categoria()
                                    subcategoria = pedir_subcategoria(categoria)
                                    tarea = Tarea(
                                                id = max([t.id for t in tareas], default=0) + 1,
                                                descripcion = descripcion,
                                                prioridad = prioridad,
                                                completada = False,
                                                categoria = Categoria(principal = categoria,
                                                                      sub = subcategoria))
                                    print(tarea)
                                    tareas.append(tarea)
                                    print("Tarea creada con exito.")
                                    guardado = False
                                except Exception as e:
                                    print(f"Error al insertar documentos: {e}")

                            case "3":
                                # 3 - Editar una tarea
                                try:
                                    continuar_submenu_editar = True
                                    while continuar_submenu_editar:
                                        utils.mostrarMenu(4)
                                        opcion_editar_tareas = input("Seleccione una opción: ")
                                        match opcion_editar_tareas:
                                            case "0":
                                                # 0 - Volver
                                                continuar_submenu_editar = False

                                            case "1":
                                                # 1 - Listar tareas
                                                utils.mostrar_tareas(tareas)

                                            case "2":
                                                # 2 - Editar tarea
                                                id = input("Id de la tarea: ")
                                                try:
                                                    tarea = utils.buscar_tareas(tareas, id)
                                                    utils.mostrar_tareas([tarea])
                                                    continuar_editar = True
                                                    while continuar_editar:
                                                        utils.mostrarMenu(5)
                                                        opcion_editar = input("Seleccione una opción: ")
                                                        match opcion_editar:
                                                            case "0":
                                                                # 0 - Volver
                                                                continuar_editar = False

                                                            case "1":
                                                                # 1 - Editar descripcion
                                                                print('Descripción actual: ', tarea.descripcion)
                                                                descripcion = input("Nueva descripcion: ")
                                                                tarea.descripcion = descripcion
                                                                print('Descripción cambiada correctamente: ', tarea.descripcion)
                                                                guardado = False

                                                            case "2":
                                                                # 2 - Editar prioridad
                                                                print('Prioridad actual: ', tarea.prioridad)
                                                                prioridad = pedir_prioridad()
                                                                tarea.prioridad = prioridad
                                                                print('Prioridad cambiada correctamente: ', tarea.prioridad)
                                                                guardado = False

                                                            case "3":
                                                                # 3 - Editar categoria
                                                                print('Categoria actual: ', tarea.categoria)
                                                                categoria = pedir_categoria()
                                                                subcategoria = pedir_subcategoria(categoria)
                                                                tarea.categoria.principal = categoria
                                                                tarea.categoria.sub = subcategoria
                                                                print('Categoria cambiada correctamente: ', tarea.categoria)
                                                                guardado = False

                                                            case "4":
                                                                # 4 - Editar subcategoria
                                                                print('Subcategoria actual: ', tarea.categoria)
                                                                subcategoria = pedir_subcategoria(tarea.categoria.principal)
                                                                tarea.categoria.sub = subcategoria
                                                                print('Subcategoria cambiada correctamente: ', tarea.categoria)
                                                                guardado = False

                                                            case _:
                                                                print("Opción no válida, intenta de nuevo.")

                                                except IndexError:
                                                    print(f"No se encontró ninguna tarea con ID {id}.")

                                            case _:
                                                print("Opción no válida, intenta de nuevo.")

                                except Exception as e:
                                    print(f"Error al editar tarea: {e}")

                            case "4":
                                # 4 - Eliminar una tarea
                                try:
                                    id = input("Id de la tarea: ")
                                    no_borrar = True
                                    while no_borrar:
                                        guardar_tarea = input("¿Seguro que quiere salir sin guardar? S/N: ")
                                        match guardar_tarea.upper():
                                            case "S":
                                                tarea = utils.buscar_tareas(tareas, id)
                                                tareas.remove(tarea)
                                                print("Tarea borrada con exito.")
                                                guardado = False
                                                no_borrar = False
                                            case "N":
                                                no_borrar = False
                                            case _:
                                                print("Opción no válida, intenta de nuevo.")
                                except Exception as e:
                                    print(f"Error al eliminar la tarea: {e}")

                            case "5":
                                # 5 - Buscar una tarea por categoría o palabra clave
                                try:
                                    categoria = input("Escriba la categoría o palabra clave: ")
                                    resultados = utils.buscar_por_palabra_clave(tareas, categoria.lower().capitalize())
                                    utils.mostrar_tareas(resultados)

                                except Exception as e:
                                    print(f"Error al guardar documentos: {e}")

                            case "6":
                                # 6 - Marcar como completada
                                try:
                                    continuar_completada = True
                                    while continuar_completada:
                                        utils.mostrarMenu(6)
                                        opcion_editar_tareas = input("Seleccione una opción: ")
                                        match opcion_editar_tareas:
                                            case "0":
                                                # 0 - Volver
                                                continuar_completada = False

                                            case "1":
                                                # 1 - Listar tareas
                                                utils.mostrar_tareas([t for t in tareas if not t.completada])

                                            case "2":
                                                # 2 - Marcar como completada
                                                id = input("Id de la tarea: ")
                                                try:
                                                    tarea = utils.buscar_tareas(tareas, id)
                                                    if tarea.completada:
                                                        print('Tarea ya completada, no se puede volver a completar.')
                                                    else:
                                                        tarea.completada = True
                                                    utils.mostrar_tareas([tarea])
                                                    guardado = False

                                                except IndexError:
                                                    print(f"No se encontró ninguna tarea con ID {id}.")

                                except Exception as e:
                                    print(f"Error al recuperar documentos: {e}")

                            case _:
                                print("Opción no válida, intenta de nuevo.")
                else:
                    print("Opción no válida, intenta de nuevo.")

            case "3":
                # 3 - Guardar cambios
                if tareas_cargadas:
                    try:
                        data_handler.guardar_lista_json(tareas)
                        if not guardado:
                            print("Tareas guardadas correctamente")
                            guardado = True
                        else:
                            print("No hay tareas para guardar")

                    except Exception as e:
                        print(f"Error al guardar los documentos: {e}")
                else:
                    print("Opción no válida, intenta de nuevo.")

            case "4":
                # 4 - Generar informe de estadísticas
                if tareas_cargadas:
                    try:
                        pass

                    except Exception as e:
                        print(f"Error al recuperar documentos: {e}")
                else:
                    print("Opción no válida, intenta de nuevo.")

            case "--help":
                try:
                    print("Documentación de las funciones del sistema")

                except Exception as e:
                    print(f"Error al recuperar documentos: {e}")

            case _:
                print("Opción no válida, intenta de nuevo.")

def pedir_prioridad():
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
    """
    Pide una subcategoría válida según la categoría principal seleccionada.
    Recibe un valor de CategoriaPrincipal.
    """
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

if __name__ == "__main__":
    main()