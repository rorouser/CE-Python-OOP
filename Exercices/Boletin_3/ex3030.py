class Bombilla():

    _encendida: bool
    estado_general: bool = True

    def __init__(self):
        self._encendida = False

    def encender(self):
        self._encendida = True

    def apagar(self):
        self._encendida = False

    def estado(self):
        if self.estado_general:
            return self._encendida
        else:
            return False

    @classmethod
    def general(cls, estado: bool):
        cls.estado_general = estado


if __name__ == "__main__":
    bombilla1 = Bombilla()
    bombilla2 = Bombilla()

    print(f"Estado bombilla 1: {bombilla1.estado()}")
    print(f"Estado bombilla 2: {bombilla2.estado()}")

    bombilla1.encender()
    print(f"Estado bombilla 1 despues de encender: {bombilla1.estado()}")
    print(f"Estado bombilla 2: {bombilla2.estado()}")

    Bombilla.general(False)
    print("Se apagan todas las bombillas")
    print(f"Estado bombilla 1: {bombilla1.estado()}")
    print(f"Estado bombilla 2: {bombilla2.estado()}")

    Bombilla.general(True)
    print("Se encienden todas las bombillas")
    print(f"Estado bombilla 1: {bombilla1.estado()}")
    print(f"Estado bombilla 2: {bombilla2.estado()}")