keys = ['Ten', 'Twenty', 'Thirty'] # Genera la lista keys
values = [10, 20, 30] # Genera la lista values
diccionario = {} #Genera un diccionario vacio.
contador = 0 # lo usaremos como índice para recorrer los valores
for key in keys: # itera la lista keys guardando en key un valorcada vez
    diccionario[key] = values[contador] # añade al diccionario el valor al que apunta "values[contador]" con clave "key"
    contador += 1 # incrementa el índice
print(diccionario)
