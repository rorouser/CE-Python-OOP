class CuentaBancaria():
    tipo: str
    tasa_interes: float

    def __init__(self, nombre, apellidos, numero_cuenta, saldo):
        self.nombre = nombre
        self.apellidos = apellidos
        self.numero_cuenta = numero_cuenta
        self.saldo = saldo

    @classmethod
    def modificar_tasa_interes(cls, nueva_tasa):
        CuentaBancaria.tasa_interes = nueva_tasa

    @classmethod
    def modificar_tipo(cls, nuevo_tipo):
        CuentaBancaria.tipo = nuevo_tipo

    def ingreso(self, cantidad):
        self.saldo += cantidad

    def retiro(self, cantidad):
        if cantidad <= self.saldo:
            self.saldo -= cantidad
        else:
            return 'Error: Fondos insuficientes'

    def aplica_tasa_interes(self):
        self.saldo += self.saldo * CuentaBancaria.tasa_interes / 100

    def __str__(self):
        return f'Cuenta de {self.nombre} {self.apellidos}\nNúmero de cuenta: {self.numero_cuenta}\nTipo de cuenta: {CuentaBancaria.tipo}\nSaldo: {self.saldo:.2f} EUR\nTasa de interés: {CuentaBancaria.tasa_interes}%\n'



if __name__ == "__main__":
    CuentaBancaria.tipo = 'Ahorro'
    CuentaBancaria.tasa_interes = 3.5

    cuenta1 = CuentaBancaria('Carlos', 'Pérez', 'ES1234567890', 1000.0)
    cuenta2 = CuentaBancaria('Laura', 'Gómez', 'ES0987654321', 2000.0)

    print(cuenta1)
    print(cuenta2)

    cuenta1.ingreso(500.0)
    cuenta2.retiro(300.0)

    print('\nDespués de operaciones:')
    print(cuenta1)
    print(cuenta2)

    cuenta1.aplica_tasa_interes()
    cuenta2.aplica_tasa_interes()

    print('\nDespués de aplicar tasa de interés:')
    print(cuenta1)
    print(cuenta2)

    CuentaBancaria.modificar_tasa_interes(4.0)
    CuentaBancaria.modificar_tipo('Nómina')

    print('\nDespués de modificar tipo y tasa de interés:')
    print(cuenta1)
    print(cuenta2)