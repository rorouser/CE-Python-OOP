class Calculadora():

    def __init__(self, variable):
        self.variable = variable

    @staticmethod
    def suma (x, y):
        return x + y

    @staticmethod
    def multiplicacion (x, y):
        return x * y

    @staticmethod
    def division (x, y):
        if y != 0:
            return x / y
        else:
            return 'Error: División por cero'

if __name__ == "__main__":
    calc = Calculadora(0)

    num1 = float(input('Ingrese el primer número: '))
    num2 = float(input('Ingrese el segundo número: '))

    print(f'Suma: {calc.suma(num1, num2)}')
    print(f'Multiplicación: {calc.multiplicacion(num1, num2)}')
    print(f'División: {calc.division(num1, num2)}')