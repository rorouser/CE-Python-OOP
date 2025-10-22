from datetime import datetime

club = dict()

def opera2(operador, apodo, fecha=datetime):
    return {
        '2': lambda: club.pop(apodo),
        '4': lambda: [print(v,k) for v, k in club.items()],
        '5': lambda: [print(v,k) for v, k in club.items()],
        '6': lambda: [print(k,v) for k, v in club.items() if k[1]>fecha.year],
        '7': lambda: False
    }.get(operador, lambda: None)

a = True
while a is True:
    op = input('''1. Alta socio.\n2. Baja socio.\n3. Modificación socio.\n4. Listar socios por apodo.\n5. Listar socios por antigüedad.\n6. Listar los socios con alta anterior a 2025\n7. Salir''')

    apodo = input('Dime tu apodo')
    nombre = input('Dime tu nombre')

    if op == '1' or op == '3':
        club[apodo] = [nombre, datetime.now()]

    if op != '7':
        opera2(op, apodo=apodo)()
    else:
        a = op



