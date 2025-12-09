from prompt_toolkit.key_binding.bindings.named_commands import capitalize_word

from SQLiteConector import SQLiteConector
import utils

# Función del programa principal
def main():
    continuar = True
    sqliteconector = None
    cargados_txt = False

    try:
        while continuar:
            utils.mostrarMenu(cargados_txt)
            opcion = input("Seleccione una opción: ")
            match opcion:
                case "0":
                    print("0")
                    continuar = False

                case "1":
                    print("1")
                    sqliteconector = SQLiteConector()
                    sqliteconector.crear_bd()
                    print(sqliteconector)

                case "2":
                    if not cargados_txt:
                        print("2")
                        if sqliteconector is None:
                            print("Error: No se ha establecido conexión con la base de datos.")
                            return
                        try:
                            oficinas = utils.leer_fichero('data/oficinas.txt', 3)
                            if oficinas:
                                sqliteconector.insertar_registros(oficinas, 'oficinas')
                                print(f"Se cargaron {len(oficinas)} oficinas correctamente")
                            empleados = utils.leer_fichero('data/empleados.txt', 5)

                            if empleados:
                                sqliteconector.insertar_registros(empleados, 'empleados')
                                print(f"Se cargaron {len(empleados)} empleados correctamente")
                            cargados_txt = True
                        except Exception as e:
                            print(f"Error al insertar documentos: {e}")
                    else:
                        print("Opción no válida.")

                case "3":
                    print("3")
                    if sqliteconector is None:
                        print("Error: No se ha establecido conexión con la base de datos.")
                        return
                    try:
                        empleados = sqliteconector.consultar_empleados()
                        print("=" * 60)
                        print("Empleados")
                        print("=" * 60)
                        if not empleados:
                            print("No se ha encontrado empleados")
                        else:
                            [print(f'{i}\n') for i in empleados]
                    except Exception as e:
                        print(f"Error al recuperar documentos: {e}")

                case "4":
                    print("4")
                    if sqliteconector is None:
                        print("Error: No se ha establecido conexión con la base de datos.")
                        return
                    try:
                        ciudad = input('Introduce la ciudad\n')
                        print("=" * 60)
                        print(f"Oficinas de {ciudad}")
                        print("=" * 60)
                        oficinas = sqliteconector.consultar_oficinas_por_ciudad(ciudad)
                        if not oficinas:
                            print("No se ha encontrado oficinas en esta ciudad")
                        else:
                            [print(f'{i}\n') for i in oficinas]
                    except Exception as e:
                        print(f"Error al recuperar documentos: {e}")

                case "5":
                    print("5")
                    if sqliteconector is None:
                        print("Error: No se ha establecido conexión con la base de datos.")
                        return
                    try:
                        edad_min = input('Introduce la edad mínima\n')
                        edad_max = input('Introduce la edad máxima\n')
                        print("=" * 60)
                        print(f"Empleados de edad entre {edad_min} y {edad_max}")
                        print("=" * 60)
                        empleados = sqliteconector.consultar_empleados_por_rango_edad(edad_min, edad_max)
                        if not empleados:
                            print("No se ha encontrado empleados en este rango de edad")
                        else:
                            [print(f'{i}\n') for i in empleados]
                    except Exception as e:
                        print(f"Error al recuperar documentos: {e}")
                case "6":
                    print("6")
                    if sqliteconector is None:
                        print("Error: No se ha establecido conexión con la base de datos.")
                        return
                    try:
                        nombre = input('Introduce el nombre del empleado\n')
                        fecha_nacimiento = input('Introduce la fecha de nacimiento del empleado (YYYY-MM-DD)\n')
                        oficina = input('Introduce la oficina del empleado\n')
                        puesto = input('Introduce el puesto del empleado\n')
                        empleado = [tuple([nombre, fecha_nacimiento, oficina, puesto, None])]
                        sqliteconector.insertar_registros(empleado, 'empleados')
                        print("Empleado insertado correctamente")
                    except Exception as e:
                        print(f"Error al insertar el empleado: {e}")

                case "7":
                    print("7")
                    if sqliteconector is None:
                        print("Error: No se ha establecido conexión con la base de datos.")
                        return
                    try:
                        calle = input('Introduce el calle de la oficina\n')
                        ciudad = input('Introduce la ciudad de la oficina\n')
                        superficie = input('Introduce la superficie de la oficina\n')
                        oficina = [tuple([calle, ciudad, superficie])]
                        sqliteconector.insertar_registros(oficina, 'oficinas')
                        print("Oficina insertada correctamente")
                    except Exception as e:
                        print(f"Error al insertar la oficina: {e}")

                case "8":
                    print("8")
                    if sqliteconector is None:
                        print("Error: No se ha establecido conexión con la base de datos.")
                        return
                    try:
                        oficina_actual = input('Empleados de la oficina\n')
                        oficina_futura = input('Oficina nueva para estos empleados\n')
                        antes, despues = sqliteconector.cambiar_oficina(oficina_actual, oficina_futura)

                        print("\n=== ANTES DEL CAMBIO ===")
                        for emp in antes:
                            print(emp)

                        print("\n=== DESPUÉS DEL CAMBIO ===")
                        for emp in despues:
                            print(emp)

                        print("\nOficinas cambiada correctamente")
                    except Exception as e:
                        print(f"Error al cambiar la oficina: {e}")

                case "9":
                    print("9")
                    if sqliteconector is None:
                        print("Error: No se ha establecido conexión con la base de datos.")
                        return
                    try:
                        print("=" * 60)
                        print("Empleados de la oficina con mayor superficie")
                        print("=" * 60)
                        empleados = sqliteconector.consultar_empleados_oficina_mayor_superficie()
                        if not empleados:
                            print("No se ha encontrado empleados")
                        else:
                            for emp in empleados:
                                print(f"ID: {emp[0]}, Nombre: {emp[1]}, Fecha Nac: {emp[2]}, "
                                      f"Oficina: {emp[3]}, Puesto: {emp[4]}, Contrato: {emp[5]}")
                                print(f"Domicilio oficina: {emp[6]}, Superficie: {emp[7]} m²\n")
                    except Exception as e:
                        print(f"Error al recuperar documentos: {e}")

                case "10":
                    print("10")
                    if sqliteconector is None:
                        print("Error: No se ha establecido conexión con la base de datos.")
                        return
                    try:
                        id_empleado = input('Introduce el ID del empleado a borrar\n')
                        confirmacion = input(f'¿Estás seguro de borrar el empleado con ID {id_empleado}? (s/n)\n')
                        if confirmacion.lower() == 's':
                            if sqliteconector.borrar_empleado(id_empleado):
                                print("Empleado borrado correctamente")
                            else:
                                print("No se pudo borrar el empleado")
                        else:
                            print("Operación cancelada")
                    except Exception as e:
                        print(f"Error al borrar el empleado: {e}")

                case "11":
                    print("11")
                    if sqliteconector is None:
                        print("Error: No se ha establecido conexión con la base de datos.")
                        return
                    try:
                        superficie_min = input('Introduce la superficie mínima\n')
                        print("=" * 60)
                        print(f"Oficinas con superficie superior a {superficie_min} m²")
                        print("=" * 60)
                        oficinas = sqliteconector.consultar_oficinas_por_superficie(superficie_min)
                        if not oficinas:
                            print("No se ha encontrado oficinas con esa superficie")
                        else:
                            [print(f'{i}\n') for i in oficinas]
                    except Exception as e:
                        print(f"Error al recuperar documentos: {e}")

                case "12":
                    print("12")
                    if sqliteconector is None:
                        print("Error: No se ha establecido conexión con la base de datos.")
                        return
                    try:
                        id_oficina = input('Introduce el ID de la oficina\n')
                        calle = input('Introduce la nueva calle\n')
                        ciudad = input('Introduce la nueva ciudad\n')
                        nuevo_domicilio = f"{calle}, {ciudad}"

                        if sqliteconector.modificar_domicilio_oficina(id_oficina, nuevo_domicilio):
                            print("Domicilio modificado correctamente")
                        else:
                            print("No se pudo modificar el domicilio")
                    except Exception as e:
                        print(f"Error al modificar el domicilio: {e}")

                case _:
                    print("Opción no válida, intenta de nuevo.")

    except Exception as e:
        print(f"Error inesperado: {e}")

    finally:
        if sqliteconector is not None:
            sqliteconector.cerrar_conexion()
        utils.borrar_base_datos()


if __name__ == "__main__":
    main()