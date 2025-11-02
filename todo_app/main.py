from datetime import datetime, timezone
import data_handler


def mostrarMenu(submenu = 0):
    if submenu == 0:
        print(" MENÚ DE OPCIONES")
        print(" 0 - Salir de la aplicacion") #añadir un desea salir sin guardar?
        print(" 1 - Cargar tareas en el sistema desde documento")
        print(" 2 - Tareas")
        print(" 3 - Guardar tareas en el documento desde el sistema")
        print(" 4 - Generar informe de estadísticas")
        print(" --help")
    if submenu == 2:
        print("     0 - Salir al menú principal")
        print("     1 - Listar tareas")
        print("     2 - Agregar una tarea")
        print("     3 - Editar una tarea")
        print("     4 - Eliminar una tarea")
        print("     5 - Buscar una tarea")
        print("     6 - Marcar como completada")




def convertir_fechas(obj):
    if isinstance(obj, dict):
        if "$date" in obj:
            return datetime.fromtimestamp(obj["$date"] / 1000, tz=timezone.utc)
        return {k: convertir_fechas(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convertir_fechas(i) for i in obj]
    else:
        return obj


# Función del programa principal
def main():
    continuar = True
    tareas = []

    while continuar:
        mostrarMenu()
        opcion = input("Seleccione una opción: ")
        match opcion:
            case "0":
                print("0")
                continuar = False

            case "1":
                try:
                    tareas = data_handler.cargar_lista_json()
                    print("Tareas cargadas correctamente")

                except FileNotFoundError as e:
                    print(f"No se pudo cargar la lista: {e}")

                except ValueError as e:
                    print(f"Error en el formato del archivo: {e}")

                except Exception as e:
                    print(f"Error inesperado: {e}")

            case "2":
                continuar_submenu = True
                while continuar_submenu:
                    mostrarMenu(2)
                    opcion_submenu = input("Seleccione una opción: ")
                    match opcion_submenu:
                        case "0":
                            print("0")
                            continuar_submenu = False

                        case "1":
                            try:
                                print(tareas)

                            except Exception as e:
                                print(f"Error al recuperar documentos: {e}")

                        case "2":
                            try:
                                pass

                            except Exception as e:
                                print(f"Error al insertar documentos: {e}")

                        case "3":
                            try:
                                pass

                            except Exception as e:
                                print(f"Error al recuperar documentos: {e}")

                        case "4":
                            try:
                                pass

                            except Exception as e:
                                print(f"Error al recuperar documentos: {e}")

                        case _:
                            print("Opción no válida, intenta de nuevo.")

            case "3":
                try:
                    pass

                except Exception as e:
                    print(f"Error al recuperar documentos: {e}")

            case "4":
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


if __name__ == "__main__":
    main()