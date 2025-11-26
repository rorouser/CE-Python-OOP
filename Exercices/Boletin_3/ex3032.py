MESES = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


class Calendario():

    def __init__(self, dia: int, mes: int, ano: int):
        self.dia = dia
        self.mes = mes
        self.ano = ano

    def incrementarDia(self):
        self.dia += 1
        if self.dia > MESES[self.mes - 1]:
            self.dia = 1
            self.mes += 1
            if self.mes > 12:
                self.mes = 1
                self.ano += 1

    def incrementarMes(self):
        self.mes += 1
        if self.mes > 12:
            self.mes = 1
            self.ano += 1

    def incrementarAno(self):
        self.ano += 1

    def mostrar(self):
        print(f"{self.dia:02d}/{self.mes:02d}/{self.ano}")

    def iguales(self, otraFecha):
        return self.dia == otraFecha.dia and self.mes == otraFecha.mes and self.ano == otraFecha.ano

if __name__ == "__main__":
    c1 = Calendario(28, 12, 2024)
    c1.incrementarDia()
    c1.incrementarDia()
    c1.incrementarDia()
    c1.mostrar()
    c2 = Calendario(4, 1, 2025)
    c2.mostrar()
    print("Fechas iguales:", c1.iguales(c2))
    c1.incrementarDia()
    c1.incrementarDia()
    c1.incrementarDia()
    c1.incrementarDia()
    c1.mostrar()
    c2.mostrar()
    print("Fechas iguales:", c1.iguales(c2))
    c1.incrementarMes()
    c1.incrementarMes()
    print("Tres meses después:")
    c1.mostrar()
    print("Un año después:")
    c1.incrementarAno()
    c1.mostrar()