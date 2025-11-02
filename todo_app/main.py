from datetime import datetime, timezone
from unittest import case
import utils
import data_handler


# Función del programa principal
def main():
    continuar = True
    tareas = []

    while continuar:
        utils.mostrarMenu()
        opcion = input("Seleccione una opción: ")
        match opcion:
            case "0":
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
                    utils.mostrarMenu(2)
                    opcion_submenu = input("Seleccione una opción: ")
                    match opcion_submenu:
                        case "0":
                            continuar_submenu = False

                        case "1":
                            try:
                                continuar_submenu_tareas = True
                                while continuar_submenu_tareas:
                                    utils.mostrarMenu(3)
                                    opcion_listar_tareas = input("Seleccione una opción: ")
                                    match opcion_listar_tareas:
                                        case "0":
                                            continuar_submenu_tareas = False

                                        case "1":
                                            utils.mostrar_tareas(tareas)

                                        case "2":
                                            utils.mostrar_tareas([t for t in tareas if t["completada"]])

                                        case "3":
                                            utils.mostrar_tareas([t for t in tareas if not t["completada"]])

                                        case _:
                                            print("Opción no válida, intenta de nuevo.")

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

                        case "5":
                            try:
                                continuar_submenu_busqueda = True
                                while continuar_submenu_busqueda:
                                    utils.mostrarMenu(4)
                                    opcion_busqueda_tareas= input("Seleccione una opción: ")
                                    match opcion_busqueda_tareas:
                                        case "0":
                                            continuar_submenu_busqueda = False

                                        case "1":
                                            pass

                                        case "2":
                                            pass

                                        case _:
                                            print("Opción no válida, intenta de nuevo.")

                            except Exception as e:
                                print(f"Error al recuperar documentos: {e}")


                        case "6":
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