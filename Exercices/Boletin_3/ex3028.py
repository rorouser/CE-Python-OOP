import os
import string
import random


class GeneradorClave():

    def __init__(self, longitud):
        self.longitud = longitud
        self.caracteresEspeciales = False
        self.numeros = True
        self.mayusculas = True
        self.minusculas = True

    def setMayusculas(self, mayusculas):
        self.mayusculas = mayusculas

    def setMinusculas(self, minusculas):
        self.minusculas = minusculas

    def setNumeros(self, numeros):
        self.numeros = numeros

    def setCaracteresEspeciales(self, caracteresEspeciales):
        self.caracteresEspeciales = caracteresEspeciales

    def modificar_longitud(self, longitud):
        self.longitud = longitud

    def generarClave(self):
        caracteres = ''
        if self.caracteresEspeciales:
            caracteres += string.punctuation
        if self.numeros:
            caracteres += string.digits
        if self.mayusculas:
            caracteres += string.ascii_uppercase
        if self.minusculas:
            caracteres += string.ascii_lowercase

        clave = ''.join(random.choice(caracteres) for _ in range(self.longitud))
        return clave

    def valoraClave(self, clave):
        valoracion = 0

        if len(clave) > 10:
            valoracion += 1
        if any(c.islower() for c in clave):
            valoracion += 1
        if any(c.isupper() for c in clave):
            valoracion += 1
        if any(c.isdigit() for c in clave):
            valoracion += 1
        if any(c in string.punctuation for c in clave):
            valoracion += 1

        return valoracion

    def guardarClave(self, clave, ruta_archivo='clave.txt'):
        with open(ruta_archivo, 'w') as archivo:
            archivo.write(clave)
        return ruta_archivo

    def leerClave(self, ruta_archivo='clave.txt'):
        if not os.path.exists(ruta_archivo):
            raise FileNotFoundError(f'El archivo {ruta_archivo} no existe.')

        with open(ruta_archivo, 'r') as archivo:
            clave = archivo.read().strip()
        return clave


if __name__ == "__main__":
    generador_clave = GeneradorClave(12)
    clave1 = generador_clave.generarClave()
    print(clave1)
    print("Robustez de la clave1 (0 es debil-5 es muy robusta): " +
          str(generador_clave.valoraClave(clave1)))
    print("- " * 20)

    generador_clave.setMayusculas(False)
    generador_clave.setMinusculas(False)
    generador_clave.setCaracteresEspeciales(True)
    clave2 = generador_clave.generarClave()
    print(clave2)
    print("Robustez de la clave2 (0 es debil-5 es muy robusta): " +
          str(generador_clave.valoraClave(clave2)))
    print("- " * 20)

    print("Guardando la clave2 ...")
    archivo = generador_clave.guardarClave(clave2)
    print(f"Clave2 guardada ok en {archivo}!")
    print("Leyendo la clave2 ...")
    print(generador_clave.leerClave())