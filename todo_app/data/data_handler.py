import json
import os
from todo_app.data.entities import *

def cargar_lista_json():
    '''
    Función para cargar la lista de tareas en el sistema
    '''
    ruta = './files/list.json'

    if not os.path.exists(ruta):
        raise FileNotFoundError(f"No se encontró el archivo de tareas")

    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            tareas = json.load(f)

            lista_personas = [Tarea.from_json(dato) for dato in tareas]

            if not isinstance(tareas, list):
                raise ValueError("El archivo JSON no contiene una lista válida de tareas.")

            return lista_personas

    except json.JSONDecodeError as e:
        raise ValueError(f"Error al decodificar JSON: {e}") from e

def guardar_lista_json(tareas):
    '''
    Función para cargar la lista de tareas en el fichero de tareas json
    '''
    try:
        tareas_dccionario = [t.to_json() for t in tareas]

        with open('../files/list.json', 'w', encoding='utf-8') as f:
            json.dump(tareas_dccionario, f, indent=4)

    except json.JSONDecodeError as e:
        raise ValueError(f"Error al decodificar JSON: {e}") from e
    except FileNotFoundError:
        print("Error: El archivo 'files/list.json' no se encontró.")