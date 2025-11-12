class Vehiculo:
    marca: str
    velocidad_inicial: int

    def __init__(self, marca, velocidad_inicial = 0):
        self.marca = marca
        self.velocidad_inicial = velocidad_inicial

    def acelerar(self, v: int):
        self.velocidad_inicial += v

    def desacelerar(self, v: int):
        self.velocidad_inicial -= v

    def mostrar_velocidad(self):
        print("Velocidad del vehículo: ", self.velocidad_inicial)

class Coche(Vehiculo):
    bocina: str

    def __init__(self, marca, velocidad_inicial, bocina = "tuuut"):
        super().__init__(marca, velocidad_inicial)
        self.bocina = bocina

    def tocar_claxon(self):
        print(self.bocina)

if __name__ == "__main__":
    mi_coche = Coche("Toyota", 20, "piiiip")
    mi_coche.mostrar_velocidad()
    mi_coche.acelerar(30)
    mi_coche.mostrar_velocidad()
    mi_coche.desacelerar(10)
    mi_coche.mostrar_velocidad()
    mi_coche.tocar_claxon()