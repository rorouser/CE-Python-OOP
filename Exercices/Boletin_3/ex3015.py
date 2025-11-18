class Empleado():
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad
        print('El emplaeado ha sido creado')

    def __del__(self):
        print('El empleado ha sido eliminado')

if __name__ == "__main__":
    empleado1 = Empleado('Juan', 30)
    empleado2 = Empleado('Ana', 25)

    print(f'Empleado 1: {empleado1.nombre}, Edad: {empleado1.edad}')
    print(f'Empleado 2: {empleado2.nombre}, Edad: {empleado2.edad}')

    del empleado1
    del empleado2