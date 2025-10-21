#Identificar al mayor y menor de la lista y también la posición en la que se encuentran

lista = [1000,6000,400,23,130,400,60,2000]

#minimum = min(zip(lista, range(len(lista))))
#maximum = max(zip(lista, range(len(lista))))

#print('Maximum: ', maximum, 'Minimum: ',minimum)

#¿Porque se borra el zip?
lista1 = zip(lista, range(len(lista)))
listalista = list(lista1)
listalista2 = list(lista1)
print(listalista)
print(listalista2)
print('Maximum: ', max(listalista))
print('Minimum: ', min(listalista))
