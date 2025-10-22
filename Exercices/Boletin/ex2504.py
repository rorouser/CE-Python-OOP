frase = input('Frase separada por espacios: ')

# Prueba con la mama de la mama de la mama de la mama de la mama no me llames
lista = frase.split(' ')
print('Palabras repetidas: ',{palabra for palabra in lista if lista.count(palabra)>1})
print('Palabras no repetidas: ',{palabra for palabra in lista if lista.count(palabra)==1})