mi_set = {1, 2, 3}
mi_set.add(6) # Agrega el elemento 6 al set
mi_set.remove(3) # Elimina el elemento 3 del set
mi_set.discard(2) # Elimina el elemento 2 si está presente
print(mi_set)

mi_otro_set = {1, 2, 3}
union_set = mi_set.union(mi_otro_set) # Une los dos sets en uno nuevo
# union_set = mi_set | mi_otro_set # Lo mismo utilizando el operador |
print('Union: ',union_set)

interseccion_set = mi_set.intersection(mi_otro_set) # Obtiene la intersección de los sets
#interseccion_set = mi_set & mi_otro_set # Lo mismo utilizando el operador &
print('Intersection: ', interseccion_set)

diferencia_set = mi_set.difference(mi_otro_set) # Obtiene la diferencia entre los sets
diferencia_set = mi_set - mi_otro_set # Lo mismo utilizando el operador -
print('Difference: ', diferencia_set)