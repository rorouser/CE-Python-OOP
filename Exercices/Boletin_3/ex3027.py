import os

class CarritoCompra():

    articulos_cantidad: dict
    articulos_precio: dict

    def __init__(self):
        self.articulos_cantidad = {}
        self.articulos_precio = {}

    def agregar_articulo(self, articulo, precio, cantidad):
        self.articulos_cantidad[articulo] = cantidad
        self.articulos_precio[articulo] = precio

    def eliminar_articulo(self, articulo):
        del self.articulos_cantidad[articulo]
        del self.articulos_precio[articulo]

    def precio_total(self):
        return sum([(vi*self.articulos_cantidad.get(ki)) for ki, vi in self.articulos_precio.items()])

    def listar_articulos(self):
        return sorted(self.articulos_cantidad.keys())

    def listar_carrito(self):
        carrito =  {(ki, self.articulos_cantidad.get(ki), vi) for ki, vi in self.articulos_precio.items()}
        if len(carrito) == 0:
            return []
        return carrito

    def costo_total_articulo(self, articulo):
        return self.articulos_cantidad.get(articulo) * self.articulos_precio.get(articulo)

    def obtener_cantidad(self, articulo):
        return self.articulos_cantidad.get(articulo)

    def contar_articulos_distintos(self):
        return len(self.articulos_cantidad.items())

    def __str__(self):
        return f'Los artículos en el carrito son: {self.listar_articulos()} \nEl costo actual del carrito es: {self.precio_total()}'

if __name__ == "__main__":

    carrito1 = CarritoCompra()
    print("Listar carrito: ", carrito1.listar_carrito())
    print("- " * 20)
    print("Agregamos 2 articulos")
    carrito1.agregar_articulo(articulo="zumo naranja", cantidad=2,
                              precio=4)
    carrito1.agregar_articulo(articulo="pan", cantidad=1.5,
                              precio=3)
    carrito1.agregar_articulo(articulo="manzana", cantidad=2,
                              precio=5)
    print("Listar carrito: ", carrito1.listar_carrito())
    print("- " * 20)
    print("La cantidad de zumo naranja seleccionado es: ",carrito1.obtener_cantidad("zumo naranja"))

    print("El costo total del pan: ",carrito1.costo_total_articulo("pan"))
    print("- " * 20)
    print("Eliminamos el pan del carrito")
    carrito1.eliminar_articulo("pan")
    print("Listar carrito: ", carrito1.listar_carrito())
    print("- " * 20)
    print("El número de artículos distintos en el carrito: ",carrito1.contar_articulos_distintos())
    print("Estado del carrito:")
    print(carrito1)
