import os

def mostrarMenu(cargados_txt: bool):
    print("=" * 60)
    print("MENÚ DE GESTIÓN DE EMPRESA")
    print("=" * 60)
    print("0 - Salir")
    if not cargados_txt:
        print("1 - Crear la base de datos Empresa con SQLite")
        print("2 - Cargar datos desde fichero empleados.txt")
    print("3 - Mostrar todos los empleados")
    print("4 - Mostrar oficinas de una ciudad determinada")
    print("5 - Mostrar empleados por rango de edad")
    print("6 - Dar de alta un nuevo empleado")
    print("7 - Dar de alta una nueva oficina")
    print("8 - Cambiar empleados de una oficina a otra")
    print("9 - Mostrar empleados de la oficina con mayor superficie")
    print("10 - Borrar un empleado")
    print("11 - Mostrar oficinas por superficie mínima")
    print("12 - Modificar domicilio de una oficina")
    print("=" * 60)


def leer_fichero(nombre_archivo, num_campos):
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            datos = []
            for numero_linea, linea in enumerate(archivo, 1):
                linea = linea.strip()
                if linea:
                    campos = linea.split(';')
                    del campos[0]
                    if len(campos) == num_campos:
                        datos.append(tuple(campos))
                    else:
                        print(
                            f"Advertencia: Línea {numero_linea} tiene {len(campos)} campos, se esperaban {num_campos}")
            return datos
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{nombre_archivo}'")
        return []
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return []

def borrar_base_datos(nombre_archivo='Empresa.db'):
    """Borra el archivo de base de datos SQLite."""
    try:
        if os.path.exists(nombre_archivo):
            os.remove(nombre_archivo)
            return True
        else:
            return False
    except Exception as e:
        print(f"Error al eliminar la base de datos: {e}")
        return False