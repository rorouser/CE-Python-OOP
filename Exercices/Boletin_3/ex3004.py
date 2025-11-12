import math

class Circulo:
    radio: int
    posicion_centro: tuple

    def __init__(self, x, y, r):
        self.radio = r
        self.posicion_centro = (x, y)

    def area(self):
        area = math.pi * self.radio ** 2
        print(f"\nEl area del circulo es {area}")

    def perimetro(self):
        perimetro = 2 * math.pi * self.radio
        print(f"\nEl perimetro del circulo es {perimetro}")

    def mostrar_propiedades(self):
        print(f"\nRadio: {self.radio} \nPosición del centro: {self.posicion_centro}")

nota = Circulo(r=5, x=1, y=2)
nota.area()
nota.perimetro()
nota.mostrar_propiedades()