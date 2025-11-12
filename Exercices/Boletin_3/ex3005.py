class Operacion:
    x: int
    y: int

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def suma(self):
        print(f"\nSuma de x + y: {self.x + self.y}")

    def multiplicacion(self):
        print(f"\nMultiplicación de x * y: {self.x * self.y}")

    def division(self):
        if self.y > 0:
            print(f"\nDivisión de x / y: {self.x / self.y}")


operacion = Operacion(x=5, y=0)
operacion.suma()
operacion.multiplicacion()
operacion.division()