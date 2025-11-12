class Nota:
    nombre_estudiante = str
    nota = int

    def __init__(self, nota, nombre_estudiante):
        self.nota = nota
        self.nombre_estudiante = nombre_estudiante

    def ha_pasado(self):
        if self.nota >= 75:
            print(f"\nEl alumno: {self.nombre_estudiante} ha aprobado con un {self.nota}")
        else:
            print(f"\nEl alumno: {self.nombre_estudiante} ha suspendido con un {self.nota}")

nota = Nota(nota=78, nombre_estudiante="Juan sin miedo")
nota2 = Nota(nota=40, nombre_estudiante="Juanito")

nota.ha_pasado()
nota2.ha_pasado()