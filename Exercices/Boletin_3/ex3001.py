class Galleta:
    nombre: str
    forma: str

    def __init__(self, nombre, forma):
        self.nombre = nombre
        self.forma = forma

    def __hornear__(self):
        print(f"Esta galleta {self.nombre} ha sido horneada en forma de {self.forma} \nBuen provecho")

if __name__ == "__main__":
    galleta = Galleta('cookies and cream', 'corazon')

    galleta.__hornear__()
