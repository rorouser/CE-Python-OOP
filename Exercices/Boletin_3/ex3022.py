class PC():

    def __init__(self, marca, modelo, precio):
        self.marca = marca
        self.modelo = modelo
        self.precio = precio

    @staticmethod
    def listar_marcas():
        return [ 'HP', 'Dell', 'Lenovo', 'Apple']

class Desktop(PC):

    def __init__(self, marca, modelo, precio, tamagno):
        super().__init__(marca, modelo, precio)
        self.tamagno = tamagno

    def mostrar_info(self):
        print(f'Marca: {self.marca}, Modelo: {self.modelo}, Precio: {self.precio}, Tamaño de la UCP: {self.tamagno} cms')

class Laptop(PC):

    def __init__(self, marca, modelo, precio, tamagno_pantalla):
        super().__init__(marca, modelo, precio)
        self.tamagno_pantalla = tamagno_pantalla

    def mostrar_info(self):
        print(f'Marca: {self.marca}, Modelo: {self.modelo}, Precio: {self.precio}, Tamaño de la pantalla: {self.tamagno_pantalla} pulgadas')

if __name__ == "__main__":
    print('Marcas disponibles:', PC.listar_marcas())

    desktop = Desktop('Dell', 'Inspiron', 700, 45)
    laptop = Laptop('Apple', 'MacBook Pro', 1500, 16)

    desktop.mostrar_info()
    laptop.mostrar_info()