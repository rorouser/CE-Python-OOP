from Exercices.Boletin_3.ex3035_maquinaria import Locomotora, Tren
from Exercices.Boletin_3.ex3035_personal import Mecanico, Maquinista, JefeEstacion

if __name__ == "__main__":
    mecanico1 = Mecanico("Pepe", "658878787", "MOTOR")
    maquinista1 = Maquinista("Manuel", "45567678F", 3400, "Secundario")
    jefeEstacion1 = JefeEstacion("Sergio", "34345345f", "25/12/2005")
    locomotora1 = Locomotora("f456", 240, 2002, mecanico1)
    tren1 = Tren(locomotora1, maquinista1)
    tren1.enganchaVagon(567, 450, "Plátanos")
    tren1.enganchaVagon(345, 345, "Plátanos")
    tren1.enganchaVagon(567, 200, "Tomates")
    tren1.enganchaVagon(567, 100, "Sandias")
    tren1.enganchaVagon(567, 156, "Peras")
    tren1.enganchaVagon(567, 345, "Plátanos")
    print(mecanico1)
    print(maquinista1)
    print(jefeEstacion1)
    print(tren1)