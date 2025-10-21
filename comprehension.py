#Listas
#[expresion for elemento in iterable if condicion]

# Crear una lista de cuadrados de números del 0 al 9
cuadrados = [x**2 for x in range(10) if x % 2 == 0]
print(cuadrados) # Salida: [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# Crear una matriz identidad de 3x3
matriz_identidad = [[1 if i == j else 0
                         for j in range(3)]
                            for i in range(3)]
print(matriz_identidad)
# Salida: [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

#Conjuntos
#{expresión for elemento in iterable if condición}
# Crear un diccionario de cuadrados solo para números pares del 0al 9
cuadrados_pares_dict = {x: x**2 for x in range(10) if x % 2 == 0}
print(cuadrados_pares_dict)
# Salida: {0: 0, 2: 4, 4: 16, 6: 36, 8: 64}

#Generadores
#(expresion for elemento in iterable if condicion)
# Crear un generador de cuadrados de números del 0 al 9
cuadrados_gen = (x**2 for x in range(10))
print(list(cuadrados_gen)) # Salida: [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]