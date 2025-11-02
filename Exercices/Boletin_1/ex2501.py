import random

def repartoAlumnos(lista, n):
    random.shuffle(lista)
    tamaño = len(lista) // n
    listas = [lista[tamaño*i : tamaño*(i+1)] for i in range(n)]
    return [print(f'Grupo {i+1}:', grupo) for i, grupo in enumerate(listas)]

lista = ['a' + str(x + 1) for x in range(50)]
repartoAlumnos(lista, 10)