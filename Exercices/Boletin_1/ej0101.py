print('Datos de la primera persona:')
nombre = input('Nombre: ')
edad = int(input('Edad: '))
altura = float(input('Altura: '))
print('Datos de la primera persona2:')
nombre2 = input('Nombre: ')
edad2 = int(input('Edad: '))
altura2 = float(input('Altura: '))

print('La persona más alta es:')
if altura > altura2:
    print(nombre)
else:
    print(nombre2)

print('La persona mayor es:')
if edad > edad2:
    print(nombre)
else:
    print(nombre2)

