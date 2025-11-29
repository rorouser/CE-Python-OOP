import random
from random import shuffle


class Colores():
    colores = "AZUL:ROJO:AMARILLO:VERDE:BLANCO:NEGRO"

    def tabla_colores(self, n: int):
        lista_colores = self.colores.split(":")
        shuffle(lista_colores)
        if 1 <= n <= len(lista_colores):
            return lista_colores[:n]
        else:
            return "Número fuera de rango"

    def sumar_color(self, name: str):
        self.colores += f":{name.upper()}"


if __name__ == "__main__":
    tc = Colores()
    tc.sumar_color("violeta")
    tc.sumar_color("magenta")
    tc.sumar_color("naranja")
    print(tc.tabla_colores(3))