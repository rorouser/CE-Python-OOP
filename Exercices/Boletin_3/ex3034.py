
class SintonizadorFM():

    def __init__(self, frecuencia: float=80.0):
        if 80.0 <= frecuencia <= 108.0:
            self.frecuencia = frecuencia
        else:
            self.frecuencia= 80.0

    def up(self):
        if self.frecuencia < 108.0:
            self.frecuencia += 0.5
        else:
            self.frecuencia = 80.0

    def down(self):
        if self.frecuencia > 80.0:
            self.frecuencia += 0.5
        else:
            self.frecuencia = 108.0

    def display(self):
        print(f'La frecuencia actual es: {self.frecuencia} MHz')


if __name__ == "__main__":
    azul = SintonizadorFM(107)
    azul.up()
    azul.up()
    azul.up()
    azul.up()
    azul.display()
    verde = SintonizadorFM(200)
    verde.display()