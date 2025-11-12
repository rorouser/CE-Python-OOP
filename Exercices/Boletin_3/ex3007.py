from Exercices.Boletin_3.ex3006 import Persona

class Estudiante(Persona):
    nivel: int

    def __init__(self, nombre, edad, genero, nivel):
        super().__init__(nombre, edad, genero)
        self.nivel = nivel

    def inscripcion(self, estudiantes_inscritos: list):
        estudiantes_inscritos.append(self)

    def __str__(self):
        return f"{self.nombre} ({self.edad} años, {self.genero}, nivel {self.nivel})"



if __name__ == "__main__":
    estudiantes_inscritos = []
    persona = Estudiante("Juanito", 10, "Masculino", 2)
    persona.inscripcion(estudiantes_inscritos)
    persona2 = Estudiante("Miguelito", 11, "Masculino", 3)
    persona2.inscripcion(estudiantes_inscritos)

    print("Estudiantes inscritos:")
    for estudiante in estudiantes_inscritos:
        print(" -", estudiante)

