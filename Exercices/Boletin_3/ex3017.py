class Micadena():

    def __init__(self, variable_str):
        self.variable_str = variable_str

    def __add__(self, cadena):
        return Micadena(self.variable_str + '|' + cadena.variable_str)

    def __len__(self):
        return len(self.variable_str)

    def __str__(self):
        return self.variable_str

    def __contains__(self, subcadena):
        return subcadena in self.variable_str

if __name__ == "__main__":
    cadena1 = Micadena('Hola')
    cadena2 = Micadena('Mundo')

    cadena3 = cadena1 + cadena2
    print(f'Cadena concatenada: {cadena3}')

    longitud = len(cadena3)
    print(f'Longitud de la cadena concatenada: {longitud}')

    subcadena = 'la'
    if subcadena in cadena3:
        print(f'La subcadena "{subcadena}" está presente en la cadena concatenada.')
    else:
        print(f'La subcadena "{subcadena}" no está presente en la cadena concatenada.')