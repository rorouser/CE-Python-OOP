import datetime

class Maquinista:
    def __init__(self, nombre: str, dni: str, sueldo: float, rango: str):
        self.nombre = nombre
        self.dni = dni
        self.sueldo = sueldo
        self.rango = rango

    def __str__(self):
        return f'Maquinista: {self.nombre} {self.dni} {self.sueldo:.1f}'

class Mecanico:
    def __init__(self, nombre: str, tlf: str, especialidad: str):
        self.nombre = nombre
        self.tlf = tlf
        self.especialidad = especialidad

    def __str__(self):
        return f'Mecánico: {self.nombre} {self.especialidad}'

class JefeEstacion:
    def __init__(self, nombre: str, dni: str, fecha_antiguedad: str):
        self.nombre = nombre
        self.dni = dni
        self.fecha_antiguedad = fecha_antiguedad

    def __str__(self):
        return f'Jefe Estación: {self.nombre} {self.dni} {datetime.datetime.strptime(self.fecha_antiguedad, "%d/%m/%Y")}'