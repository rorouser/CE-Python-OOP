import collections


class Cola():

    def __init__(self):
        self.cola: collections.deque = collections.deque()

    def insertar(self, elemento):
        self.cola.append(elemento)

    def extraer(self):
        if not self.numeroElementos():
            return None
        return self.cola.popleft()

    def numeroElementos(self):
        return len(self.cola)

    def mostrar(self):
        print([i for i in self.cola])

if __name__ == "__main__":
    c1 = Cola()
    c1.insertar(25)
    c1.insertar(212)
    c1.insertar(13)
    c1.insertar(2)
    c1.insertar(22)
    c1.insertar(11)
    c1.insertar(4)
    c1.insertar(23)
    c1.mostrar()
    print("Número de elementos: ", c1.numeroElementos())
    print("Extrae:", c1.extraer())
    print("Extrae:", c1.extraer())
    print("Extrae:", c1.extraer())
    c1.mostrar()