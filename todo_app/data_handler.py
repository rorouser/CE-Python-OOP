import json
import os

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

            if not isinstance(tareas, list):
                raise ValueError("El archivo JSON no contiene una lista válida de tareas.")

            return tareas

    except json.JSONDecodeError as e:
        raise ValueError(f"Error al decodificar JSON: {e}") from e

def escribir_lista_json():
    with open('files/list.json', 'w', encoding='utf-8') as f:
        json.dump(cargar_lista_json(), f)