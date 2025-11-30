from Exercices.Boletin_3.ex3035_personal import Mecanico, Maquinista


class Vagones:
    def __init__(self, id: str, carga_maxima: float, carga_actual: float, tipo_mercancia: str):
        self.id = id
        self.carga_maxima = carga_maxima
        self.carga_actual = carga_actual
        self.tipo_mercancia = tipo_mercancia

class Locomotora:
    def __init__(self, matricula: str, potencia_motor: float, antiguedad: int, mecanico: Mecanico):
        self.matricula = matricula
        self.potencia_motor = potencia_motor
        self.antiguedad = antiguedad
        self.mecanico = mecanico

class Tren:
    def __init__(self, locomotora: Locomotora, maquinista: Maquinista, vagones: list[Vagones] = []):
        self.locomotora = locomotora
        self.vagones = vagones
        self.maquinista = maquinista

    def enganchaVagon(self, id: str, carga_maxima: float, tipo_mercancia: str):
        vagon = Vagones(id, carga_maxima, 0, tipo_mercancia)
        if len(self.vagones) < 5:
            self.vagones.append(vagon)
        else:
            print('Error !! el tren no admite más vagones')

    def __str__(self):
        info_vagones = ''
        for i, vagon in enumerate(self.vagones, 1):
            info_vagones += f'      Vagón {i} Mercancía: {vagon.tipo_mercancia}\n'
        return (f'Componentes del tren: \n'
                f'  Locomotora: {self.locomotora.matricula} \n'
                f'  Maquinista: {self.maquinista.nombre} \n'
                f'{info_vagones}').strip()