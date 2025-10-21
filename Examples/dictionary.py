mi_diccionario = {"nombre": "Luis", "altura": 30, "profesion":
"Ingeniero"}

print(mi_diccionario["nombre"]) # Resultado: Luis
print(mi_diccionario["altura"]) # Resultado: 30

mi_diccionario["clave1"] = 12312142
mi_diccionario["nueva_clave"] = 4134313
mi_diccionario["ciudad"] = "Madrid"

print(mi_diccionario)

vista_items = mi_diccionario.items() # Retorna una vista de los pares clave-valor
print(vista_items)

claves = mi_diccionario.keys() # Devuelve una lista de las claves
valores = mi_diccionario.values()
print(claves)
print(valores)

del mi_diccionario["altura"] # Elimina una clave y su valor
valor_eliminado = mi_diccionario.pop("clave1") # Elimina y devuelve el valor de una clave
print(valor_eliminado)
print(mi_diccionario)

mi_diccionario.clear() # Elimina todos los elementos del diccionario
print(mi_diccionario) # Resultado: {}


sampleDict = {
    "class":{
        "student":{
            "name":"Mike",
            "marks":{
            "physics":70,
            "history":80
            }
        }
    }
}

print(sampleDict["class"]['student']['marks']['history'])