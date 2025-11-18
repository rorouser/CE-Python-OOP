class Trabajador():
    def __init__(self, nombre, salario, edad):
        self.nombre = nombre
        self.salario = salario
        self.edad = edad

    def mostrar_funcion(self):
        print('Soy un trabajador')

    def mostrar_info(self):
        print(f'Nombre: {self.nombre}, Salario: {self.salario}, Edad: {self.edad}')

class Director(Trabajador):
    def __init__(self, nombre, salario, edad, prima):
        super().__init__(nombre, salario, edad)
        self.prima = prima

    def mostrar_funcion(self):
        print('Soy director de la empresa')

    def mostrar_info(self):
        super().mostrar_info()
        print(f'Prima: {self.prima}')

class Ingeniero(Trabajador):
    def __init__(self, nombre, salario, edad, especialidad):
        super().__init__(nombre, salario, edad)
        self.especialidad = especialidad

    def mostrar_funcion(self):
        print('Soy un ingeniero')

    def mostrar_info(self):
        super().mostrar_info()
        print(f'Especialidad: {self.especialidad}')

if __name__ == "__main__":
    director = Director('Carlos', 80000, 50, 15000)
    ingeniero = Ingeniero('Laura', 60000, 35, 'Software')

    director.mostrar_funcion()
    director.mostrar_info()

    ingeniero.mostrar_funcion()
    ingeniero.mostrar_info()