print('Introduce el email:')
email = input('Email: ').count('@')

if email == 1:
    print('Contiene un caracter')
else:
    print('Contiene más de un caracter o no contiene, email incorrecto')