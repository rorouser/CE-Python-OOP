print('Ingresar clave:')
email = len(input('Clave: '))

if email > 21 or email < 11:
    print('Error')
else:
    print('Clave correcta')