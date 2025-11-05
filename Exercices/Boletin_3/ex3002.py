class Libro:
    titulo = str
    nombre_autor = str
    precio = float

    def __init__(self, titulo, nombre_autor, precio):
        self.titulo = titulo
        self.nombre_autor = nombre_autor
        self.precio = precio

    def mostrar_informaciones(self):
        print(f"\nTitulo: {self.titulo} Precio: {self.precio} Autor: {self.titulo} ")

libro = Libro(titulo='cookies and cream', precio=10.50, nombre_autor='corazon')

libro.mostrar_informaciones()