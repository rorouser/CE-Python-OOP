from prompt_toolkit.key_binding.bindings.named_commands import capitalize_word

from SQLiteConector import SQLiteConector
import utils

# Función del programa principal
def main():
    continuar = True
    sqliteconector= None
    nombreColeccion = "restaurantes"
    
    while continuar:
        utils.mostrarMenu()
        opcion = input("Seleccione una opción: ")
        match opcion:
            case "0":
                # Finalizar el programa sin usar el break
                print ("0")
                continuar = False

            case "1":
                # Crear la conexión a la BBDD y guardar en variable
                print("1")
                sqliteconector = SQLiteConector()
                sqliteconector.crear_bd()
                print(sqliteconector)

            case "2":
                # Cargar el fichero y realizar el insert a la base de datos siempre que se haya establecido la conexión con la base de datos
                print ("2")
                if sqliteconector is None:
                    print("Error: No se ha establecido conexión con la base de datos.")
                    return
                try:
                    oficinas = utils.leer_fichero('data/oficinas.txt', 4)

                    if oficinas:
                        sqliteconector.insertar_registros(oficinas, 'oficinas')
                        print(f"Se cargaron {len(oficinas)} oficinas correctamente")

                    # Leer empleados con 7 campos (pero solo usar 6)
                    empleados = utils.leer_fichero('data/empleados.txt', 6)

                    if empleados:
                        sqliteconector.insertar_registros(empleados, 'empleados')
                        print(f"Se cargaron {len(empleados)} empleados correctamente")

                except Exception as e:
                        print(f"Error al insertar documentos: {e}")

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
                    empleados = sqliteconector.consultar_oficinas_por_rango_edad(edad_min, edad_max)
                    if not empleados:
                        print("No se ha encontrado empleados en este rango de edad")
                    else:
                        [print(f'{i}\n') for i in empleados]
                    [print(f'{i}\n') for i in empleados]
                except Exception as e:
                    print(f"Error al recuperar documentos: {e}")
            case "6":
                # Mostrar los cinco restaurantes con mejor calificación promedio siempre que se haya establecido la conexión con la base de datos
                print ("6")
                if conexion is None:
                    print("Error: No se ha establecido conexión con la base de datos.")
                    return 
                try:

                    pipeline = [
                        {"$unwind": "$notas"},
                        {"$match": {"notas.puntuacion": {"$exists": True, "$ne": None}}},  # Filtrar puntuaciones nulas
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
                            "_id": "$nombre",
                            "calificacion_promedio": {"$avg": "$notas.puntuacion"}
                        }},
                        {"$sort": {"calificacion_promedio": -1}},
                        {"$limit": 5},
                        {"$project": {
                            "_id": 0,
                            "nombre": "$_id",
                            "promedio": {"$round": ["$calificacion_promedio", 2]}
                        }}
                    ]


                    restaurantes = conexion.obtenerAgregacion(nombreColeccion, pipeline)

                    if restaurantes:
                        print("Los cinco restaurantes con mejor calificación promedio:")
                        for restaurante in restaurantes:
                            print(f"- {restaurante['nombre']}: {restaurante['promedio']:.2f}")
                    else:
                        print("No se encontraron datos.")
                except Exception as e:
                        print(f"Error al recuperar documentos: {e}")

            case "7":
                # Insertar una nota a un restaurante siempre que se haya establecido la conexión con la base de datos.
                print("7")
                if conexion is None:
                    print("Error: No se ha establecido conexión con la base de datos.")
                    return
                
                try:
                    # Solicitar ID del restaurante en un bucle hasta que se encuentre uno válido
                    while True:
                        restaurante_id = input("Introduce el ID del restaurante: ")
                        if not restaurante_id:
                            print("El ID no puede estar vacío.")
                            continue
                        
                        # Verificar si el restaurante existe
                        restaurante = conexion.encontrarDocumento(nombreColeccion, {"restaurante_id": restaurante_id})
                        
                        if restaurante:
                            break  
                        else:
                            print("Error: No se encontró un restaurante con ese ID. Inténtalo de nuevo.")

                    # Validar la calificación
                    calificaciones_validas = {"A", "B", "C", "P", "Z"}
                    while True:
                        calificacion = input("Introduce la calificación (A, B, C, P, Z): ").strip().upper()
                        if calificacion in calificaciones_validas:
                            break
                        print("Error: Calificación no válida. Debe ser A, B, C, P o Z.")

                    # Validar la puntuación
                    while True:
                        try:
                            puntuacion = int(input("Introduce la puntuación (0-50): ").strip())
                            if 0 <= puntuacion <= 50:
                                break
                            print("Error: La puntuación debe estar entre 0 y 50.")
                        except ValueError:
                            print("Error: Debes introducir un número válido.")

                    # Obtener fecha actual en formato Unix timestamp (milisegundos)
                    fecha_actual = int(datetime.now(timezone.utc).timestamp() * 1000)
                    
                    fecha_h = datetime.fromtimestamp(fecha_actual / 1000, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

                    # Crear la nueva nota
                    nueva_nota = {
                        "fecha": {"$date": fecha_actual},
                        "calificacion": calificacion,
                        "puntuacion": puntuacion
                    }

                    # Insertar la nota en la lista "notas" del restaurante
                    resultado = conexion.insertarEnLista(nombreColeccion, restaurante_id, "notas", nueva_nota)

                    if resultado.modified_count > 0:
                        print(f"Nota agregada correctamente.\nCalificación: {calificacion}\nPuntuación: {puntuacion}\nFecha: {fecha_h}")
                    else:
                        print("No se pudo agregar la nota.")

                except Exception as e:
                    print(f"Error al insertar la nota: {e}")

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