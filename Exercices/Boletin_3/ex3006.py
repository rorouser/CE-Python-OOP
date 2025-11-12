class Persona:
    nombre: str
    edad: int
    genero: str

    def __init__(self, nombre, edad, genero):
        self.nombre = nombre
        self.edad = edad
        self.genero = genero

    def presentarse(self):
        print(f"\nSoy {self.nombre} y tengo {self.edad} con género {self.genero} ")

    def esAdulto(self):
        if self.edad >= 18:
            return True
        else:
            return False


if __name__ == "__main__":
    persona = Persona("Juanito", 10 , "Masculino")
    persona.presentarse()
    print("Es adulto" if persona.esAdulto() else "Es menor de edad")