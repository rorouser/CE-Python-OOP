print('Datos de la primera persona:')
nombre = input('Nombre: ').lower()

if nombre[0]=='a' or nombre[0]=='e' or nombre[0]=='i' or nombre[0]=='o' or nombre[0]=='u':
    print('Empieza por vocal', nombre)
else:
    print('No empieza por vocal', nombre)

