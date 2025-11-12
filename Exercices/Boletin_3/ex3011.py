import math

class Calculo_numerico:
    numero: int

    def __init__(self, numero):
        self.numero = numero

    def calculo_factorial(self):
        if self.numero < 0:
            return "El número debe ser natural"
        else:
            return math.factorial(self.numero)

    def lista_divisores(self) -> list:
        return sorted([i for i in range(1, self.numero + 1) if self.numero % i == 0])

    def esPrimo(self):
        if len(self.lista_divisores()) <= 2:
            print("Es primo")
        else:
            print("No es primo")

    def esPar(self):
        if self.numero % 2 == 0:
            print("Es par")
        else:
            print("No es par")

    def info_funcion(self) -> str:
        return self.funcion

if __name__ == "__main__":
    calc = Calculo_numerico(13)
    print("Factorial:", calc.calculo_factorial())
    print("Divisores:", calc.lista_divisores())
    calc.esPrimo()
    calc.esPar()