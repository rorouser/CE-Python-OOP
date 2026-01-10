
class Libro:
    """Clase que representa un libro en la biblioteca"""

    def __init__(self, titulo: str, autor: str, isbn: str):
        self.__titulo = titulo
        self.__autor = autor
        self.__isbn = isbn
        self.__disponible = True

    @property
    def titulo(self) -> str:
        return self.__titulo

    @property
    def autor(self) -> str:
        return self.__autor

    @property
    def isbn(self) -> str:
        return self.__isbn

    @property
    def disponible(self) -> bool:
        return self.__disponible

    def prestar(self) -> bool:
        """Marca el libro como prestado"""
        if self.__disponible:
            self.__disponible = False
            return True
        return False

    def devolver(self) -> None:
        """Marca el libro como disponible"""
        self.__disponible = True

    def __str__(self) -> str:
        estado = "Disponible" if self.__disponible else "Prestado"
        return f"'{self.__titulo}' - Autor: {self.__autor}, ISBN: {self.__isbn}, Estado: {estado}"

class Biblioteca:
    __nombre: str
    __libros: list[Libro]

    def __init__(self, nombre, libros):
        self.__nombre = nombre
        self.__libros = libros

    def agregar_libro(self, libro: Libro):
        self.__libros.append(libro)

    def mostrar_libros(self):
        for libro in self.__libros:
            print(libro)

    def buscar_por_titulo(self, titulo: str):
        for libro in self.__libros:
            if libro.titulo == titulo:
                return libro
        return None

    def prestar_libro(self, isbn: str):
        for libro in self.__libros:
            if libro.isbn == isbn and libro.disponible:
                libro.prestar()
                print('Libro prestado con éxito.')
            else:
                print('El libro no está disponible para préstamo.')