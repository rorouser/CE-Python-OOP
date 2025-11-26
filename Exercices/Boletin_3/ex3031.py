EUROS_DICT = {
    "Billetes 500€": 500.00,
    "Billetes 200€": 200.00,
    "Billetes 100€": 100.00,
    "Billetes 50€": 50.00,
    "Billetes 20€": 20.00,
    "Billetes 10€": 10.00,
    "Billetes 5€": 5.00,
    "Monedas 2€": 2.00,
    "Monedas 1€": 1.00,
    "Monedas 50 cent": 0.50,
    "Monedas 20 cent": 0.20,
    "Monedas 10 cent": 0.10,
    "Monedas 5 cent": 0.05,
    "Monedas 2 cent": 0.02,
    "Monedas 1 cent": 0.01
}

class CambioMonedas():
    importeCompra: float
    dineroCliente: float

    def __init__(self, importeCompra, dineroCliente):
        self.importeCompra = importeCompra
        self.dineroCliente = dineroCliente

    def mostrar_cambio(self):
        cambio = round(self.dineroCliente - self.importeCompra, 2)

        if self.dineroCliente < self.importeCompra:
            print(f'Error!! Faltan {abs(cambio)}\nCambio resultante de 0.00:\n* * * * * * * * * *')
            return

        print(f'Cambio resultante de {cambio}:')

        desglose = {}
        for nombre, valor in EUROS_DICT.items():
            cantidad = int(cambio // valor)
            if cantidad > 0:
                desglose[nombre] = cantidad
                cambio = round(cambio - (cantidad * valor), 2)

        for nombre, cantidad in desglose.items():
            print(f'{nombre}: {cantidad}')
        print("* * * * * * * * * *")


if __name__ == "__main__":
    c1 = CambioMonedas(215.35, 250)
    c1.mostrar_cambio()
    c2 = CambioMonedas(100, 80)
    c2.mostrar_cambio()
    c3 = CambioMonedas(75.75, 90)
    c3.mostrar_cambio()