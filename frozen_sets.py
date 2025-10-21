# Crear un frozenset a partir de una lista
conjunto_inmutable = frozenset([1, 2, 3, 4, 5])
print(conjunto_inmutable) # Salida: frozenset({1, 2, 3, 4, 5})
# Crear un frozenset a partir de una lista de strings
frutas = frozenset(["manzana", "banana", "naranja"])
print(frutas) # Salida: frozenset({'manzana', 'banana','naranja'})
# Crear un frozenset a partir de un set
conjunto_mutable = {1, 2, 3, 4, 5}
conjunto_inmutable = frozenset(conjunto_mutable)
print(conjunto_inmutable) # Salida: frozenset({1, 2, 3, 4, 5})
# Crear un frozenset a partir de una cadena
conjunto_inmutable = frozenset('python')
print(conjunto_inmutable) # Salida: frozenset({'p', 'y', 't','h', 'o', 'n'})


# Crear dos frozensets
set_a = frozenset([1, 2, 3])
set_b = frozenset([3, 4, 5])
# Unión de frozensets
union_set = set_a | set_b
print(union_set) # Salida: frozenset({1, 2, 3, 4, 5})
# Intersección de frozensets
interseccion_set = set_a & set_b
print(interseccion_set) # Salida: frozenset({3})
# Diferencia de frozensets
diferencia_set = set_a - set_b
print(diferencia_set) # Salida: frozenset({1, 2})
# Diferencia simétrica de frozensets
diferencia_simetrica_set = set_a ^ set_b
print(diferencia_simetrica_set) # Salida: frozenset({1, 2, 4, 5})
# Diferencia simétrica de frozensets
isSubet = frozenset([3, 4]) < set_b
print(isSubet) # True