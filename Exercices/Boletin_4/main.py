from prompt_toolkit.key_binding.bindings.named_commands import capitalize_word

from SQLiteConector import SQLiteConector
import utils

# Función del programa principal
def main():
    continuar = True
    sqliteconector= None
    cargados_txt = False
    
    while continuar:
        utils.mostrarMenu(cargados_txt)
        opcion = input("Seleccione una opción: ")
        match opcion:
            case "0":
                print ("0")
                if sqliteconector is not None:
                    sqliteconector.cerrar_conexion()
                utils.borrar_base_datos()
                continuar = False

            case "1":
                print("1")
                sqliteconector = SQLiteConector()
                sqliteconector.crear_bd()
                print(sqliteconector)

            case "2":
                if not cargados_txt:
                    print ("2")
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
                print ("3")
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
                    contrato = input('Introduce el tipo de contrato del empleado\n')
                    empleado = [tuple([nombre, fecha_nacimiento, oficina, puesto, contrato])]
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
                # Encontrar el mejor restaurante de cada distrito según su puntuación media.
                print ("8")
                if conexion is None:
                    print("Error: No se ha establecido conexión con la base de datos.")
                    return 
                
                try:
                    pipeline = [
                        {"$unwind": "$notas"},
                        {"$match": {"notas.puntuacion": {"$exists": True, "$ne": None}}},
                        {"$addFields": {
                            "notas.puntuacion": {
                                "$convert": {
                                    "input": "$notas.puntuacion",
                                    "to": "double",
                                    "onError": 0,
                                    "onNull": 0
                                }
                            }
                        }},
                        {"$group": {
                            "_id": {"nombre": "$nombre", "distrito": "$distrito"},
                            "calificacion_promedio": {"$avg": "$notas.puntuacion"}
                        }},
                        {"$sort": {"_id.distrito": 1, "calificacion_promedio": -1}},
                        {"$group": {
                            "_id": "$_id.distrito",
                            "mejor_restaurante": {"$first": "$_id.nombre"},
                            "puntuacion": {"$first": "$calificacion_promedio"}
                        }},
                        {"$project": {
                            "_id": 0,
                            "distrito": "$_id",
                            "nombre": "$mejor_restaurante",
                            "puntuacion": {"$round": ["$puntuacion", 2]}
                        }},
                        {"$sort": {"distrito": 1}}
                    ]

                    mejores_restaurantes = conexion.obtenerMejoresRestaurantesPorDistrito(nombreColeccion, pipeline)
                    if mejores_restaurantes:
                        print("Mejor restaurante por distrito:")
                        for restaurante in mejores_restaurantes:
                            print(f"- Distrito: {restaurante['distrito']}, Restaurante: {restaurante['nombre']} ({restaurante['puntuacion']:.2f})")
                    else:
                        print("No se encontraron datos.")
                except Exception as e:
                    print(f"Error al recuperar documentos: {e}")
                
            case "9":
                # Borrar todos los documentos siempre que se haya establecido la conexión con la base de datos.
                print ("9")
                if conexion is None:
                    print("Error: No se ha establecido conexión con la base de datos.")
                    return 
                try:
                    documentos_eliminados = conexion.borrarDocumentosColeccion(nombreColeccion)
                    print(f"Se han eliminado {documentos_eliminados} documentos.")
                except Exception as e:
                    print(f"Error al borrar los documentos: {e}")
            case "10":
                # Cerrar conexión siempre que se haya establecido la misma anteriormente.
                print ("10")
                if conexion is None:
                    print("Error: No se ha establecido conexión con la base de datos.")
                    return 
                try:
                    conexion.cerrarConexion()
                except Exception as e:
                        print(f"Error al cerrar la conexión: {e}")
                
            case _:
                 print("Opción no válida, intenta de nuevo.")
            
        

if __name__ == "__main__":
    main()    