class CuentaCorriente():
    banco = "Banco Python"

    def __init__(self, dni: str, nombre: str, saldo: float = 0.0, gestor=None):
        self.dni = dni
        self.nombre = nombre
        self.saldo = saldo
        self.gestor = gestor

    def sacar_dinero(self, cantidad: float):
        if cantidad > self.saldo:
            print("Saldo insuficiente")
        else:
            self.saldo -= cantidad

    def ingresar(self, cantidad: float):
        self.saldo += cantidad

    def mostrar(self):
        gestor_info = f"\nGestor: {self.gestor.nombre}" if self.gestor else ""
        print(
            f"Cuenta de {CuentaCorriente.banco} \nCuenta de {self.nombre} \n(DNI: {self.dni})\nSaldo: {self.saldo:.2f} EUR{gestor_info}")

    def __str__(self):
        gestor_info = f", Gestor: {self.gestor.nombre}" if self.gestor else ", Sin gestor"
        return f"Cuenta de {self.nombre} (DNI: {self.dni}) - Saldo: {self.saldo:.2f}€{gestor_info}"


class Gestor:
    def __init__(self, nombre, tfno, importe_maximo=10000):
        self.nombre = nombre
        self.tfno = tfno
        self.importe_maximo = importe_maximo

    def __str__(self):
        return f"Gestor: {self.nombre}, Tfno: {self.tfno}, Importe máximo: {self.importe_maximo}€"


if __name__ == "__main__":
    CuentaCorriente.banco = "Banco Santander"

    gestor1 = Gestor("María García", "600123456", 15000)
    gestor2 = Gestor("Carlos López", "600654321")

    cuenta1 = CuentaCorriente("12345678A", "Juan Pérez", 0.0, gestor1)
    cuenta2 = CuentaCorriente("87654321B", "Ana Martínez")
    cuenta3 = CuentaCorriente("11223344C", "Luis Rodríguez", 0.0, gestor2)

    cuenta1.mostrar()
    cuenta1.ingresar(1000)
    cuenta1.sacar_dinero(300)
    cuenta1.sacar_dinero(800)

    cuenta2.mostrar()
    cuenta2.ingresar(500)

    print("\n=== Resumen de cuentas ===")
    print(cuenta1)
    print(cuenta2)
    print(cuenta3)