class Empleado:
    nombre: str
    funcion: str
    salario: int
    num_horas: int

    def __init__(self, nombre, funcion, salario):
        self.nombre = nombre
        self.funcion = funcion
        self.salario = salario
        self.num_horas = 0

    def trabajar(self, num_horas) -> str:
        self.num_horas += num_horas
        return str(self.num_horas) + " horas"

    def info_sueldo(self) -> str:
        return str(self.salario) + " €"

    def dar_aumento(self,cantidad):
        self.salario += cantidad

    def info_funcion(self) -> str:
        return self.funcion

if __name__ == "__main__":
    emp = Empleado("Ana", "Programadora", 2000)

    print(emp.info_funcion())
    print("Salario:", emp.info_sueldo())

    print("Horas trabajadas:", emp.trabajar(5))
    print("Horas trabajadas:", emp.trabajar(3))

    emp.dar_aumento(300)
    print("Salario después del aumento:", emp.info_sueldo())