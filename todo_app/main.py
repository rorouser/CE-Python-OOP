from datetime import datetime, timezone
from unittest import case
import utils
import data_handler
from entities import Tarea, Categoria, Prioridad

# Función del programa principal
def main():
    continuar = True
    tareas = []
    tareas_cargadas = False
    while continuar:
        utils.mostrarMenu(tareas_cargadas=tareas_cargadas)
        opcion = input("Seleccione una opción: ")
        match opcion:
            case "0":
                # 0 - Salir de la aplicacion
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
                                            utils.mostrar_tareas([t for t in tareas if t["completada"]])

                                        case "3":
                                            # 3 - Listar tareas pendientes
                                            utils.mostrar_tareas([t for t in tareas if not t["completada"]])

                                        case _:
                                            print("Opción no válida, intenta de nuevo.")

                            except Exception as e:
                                print(f"Error al recuperar documentos: {e}")

                        case "2":
                            # 2 - Agregar una tarea
                            try:
                                descripcion = input("Descripción: ")
                                opciones = [p.value for p in Prioridad]
                                print(f"Opciones de prioridad: {', '.join(o.capitalize() for o in opciones)}")
                                prioridad = input("Prioridad: ")
                                categoria = input("Categoria: ")
                                subcategoria = input("Subcategoria: ")
                                tareas.append(Tarea(
                                            id = max([t["id"] for t in tareas], default=0) + 1,
                                            descripcion = descripcion,
                                            prioridad = prioridad,
                                            completada = False,
                                            categoria = Categoria(principal = categoria,
                                                                  sub = subcategoria)))
                                print("Tarea creada con exito.")
                            except Exception as e:
                                print(f"Error al insertar documentos: {e}")

                        case "3":
                            # 3 - Editar una tarea
                            try:
                                pass

                            except Exception as e:
                                print(f"Error al recuperar documentos: {e}")

                        case "4":
                            # 4 - Eliminar una tarea
                            try:
                                pass

                            except Exception as e:
                                print(f"Error al recuperar documentos: {e}")

                        case "5":
                            # 5 - Buscar una tarea por categoría o palabra clave
                            try:
                                categoria = input("Escriba la categoría o palabra clave: ")
                                resultados = utils.buscar_por_categoria(tareas, categoria)
                                utils.mostrar_tareas(resultados)

                            except Exception as e:
                                print(f"Error al recuperar documentos: {e}")

                        case "6":
                            # 6 - Marcar como completada
                            try:
                                pass

                            except Exception as e:
                                print(f"Error al recuperar documentos: {e}")

                        case _:
                            print("Opción no válida, intenta de nuevo.")

            case "3":
                # 3 - Guardar cambios
                try:
                    data_handler.guardar_lista_json(tareas)
                    print("Tareas guardadas correctamente")

                except Exception as e:
                    print(f"Error al recuperar documentos: {e}")

            case "4":
                # 4 - Generar informe de estadísticas
                try:
                    pass

                except Exception as e:
                    print(f"Error al recuperar documentos: {e}")

            case "--help":
                try:
                    print("Documentación de las funciones del sistema")

                except Exception as e:
                    print(f"Error al recuperar documentos: {e}")


            case _:
                print("Opción no válida, intenta de nuevo.")

def pedir_prioridad():
    # 🔹 Mostrar las prioridades disponibles
    opciones = [p.value for p in Prioridad]  # ["alta", "media", "baja"]
    print(f" Opciones de prioridad: {', '.join(o.capitalize() for o in opciones)}")

    # 🔹 Pedir al usuario hasta que elija una válida
    while True:
        entrada = input(" Prioridad: ").strip().lower()
        if entrada in opciones:
            return Prioridad(entrada)
        print(" Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()