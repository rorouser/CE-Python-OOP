# Uso básico de reduce():
from functools import reduce

def suma(x, y):
    return x + y

numeros = [1, 2, 3, 4, 5]
suma_total = reduce(suma, numeros)
print(suma_total) # Salida: 15