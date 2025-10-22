import random

def repartoAlumnos (lista, n):
    random.shuffle(lista)
    listas = [lista[(len(lista)//n)*i:(len(lista)//n)+(len(lista)//n)*i] for i in range(n)]
    return [print('Grupo ', lista) for lista in listas]

lista = ['a' + str(x + 1) for x in range(50)]
repartoAlumnos(lista, 5)