import random

class Dado:
    marca: int

    def __init__(self, marca = 0):
        self.marca = marca

    def lanzar_dado(self):
        self.marca = random.randint(1, 6)

    def mostrar_puntos(self):
        print("Resultado: ", self.marca)


if __name__ == "__main__":
    dado = Dado()
    dado.lanzar_dado()
    dado.mostrar_puntos()