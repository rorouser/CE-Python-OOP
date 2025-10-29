from datetime import datetime

club = dict()

def opera2(operador, apodo='', nombre='', fecha=datetime):
    if operador == '1':
        club[apodo] = [nombre, datetime.now().strftime('%d/%m/%Y %H:%M:%S')]
        print(f'Socio {apodo} dado de alta.')
    elif operador == '2':
        if apodo in club:
            club.pop(apodo)
            print(f'Socio {apodo} eliminado.')
        else:
            print('Ese apodo no existe.')
    elif operador == '3':
        if apodo in club:
            club[apodo] = [nombre,  datetime.now().strftime('%d/%m/%Y %H:%M:%S')]
            print(f'Socio {apodo} modificado.')
        else:
            print('Ese apodo no existe.')
    elif operador == '4':
        [print(v, k) for v, k in club.items()]
    elif operador == '5':
        [print(v, k) for v, k in club.items()]
    elif operador == '6':
        [print(k, v) for k, v in club.items() if datetime.strptime(v[1], '%d/%m/%Y %H:%M:%S').year < fecha.now().year]
    elif operador == '7':
        return False
    else:
        print('Opción no válida.')
    return True

a = True
while a:
    op = input('''\n1. Alta socio.\n2. Baja socio.\n3. Modificación socio.\n4. Listar socios por apodo.\n5. Listar socios por antigüedad.\n6. Listar los socios con alta anterior a 2025.\n7. Salir\n> ''')
    if op in ('1', '2', '3'):
        apodo = input('Dime tu apodo: ')
        nombre = input('Dime tu nombre: ')
    else:
        apodo = ''
        nombre = ''
    a = opera2(op, apodo, nombre)
