def obtener_datos_persona():
    nombre = "Luis"
    edad = 30
    return nombre, edad
datos = obtener_datos_persona()
nombre, edad = datos
print(nombre, edad)

persona1 = ("Luis", 30)
persona2 = ("Ana", 25)
diccionario_personas = {persona1: "Programador", persona2:
"Diseñador"}

print(diccionario_personas)