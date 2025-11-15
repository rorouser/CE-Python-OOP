from random import randint

columna1 = ('integrated', 'total', 'systematized', 'parallel', 'functional',
'responsive', 'optimal', 'synchronized', 'compatible', 'balanced')
columna2 = ('management', 'organizational', 'monitored', 'reciprocal',
'digital', 'logistical', 'transitional', 'incremental',
'third-generation', 'policy')

columna3 = ('options', 'flexibility', 'capability', 'mobility', 'programming',
'concept', 'time-phase', 'projection', 'hardware', 'contingency')

lista = [columna1, columna2, columna3]

def generateRandomBuzzWord():
    """Genera 3 cifras aleatorias y obtiene el buzzword correspondiente"""
    return ''.join([lista[i][[randint(1, 9) for i in range(3)][i]]
                    for i in range(len(lista))])

def generateBuzzWord(id):
    """Usamos un único número de 3 cifras (entre 0 y 999) que define nuestro buzzWord"""
    return ''.join([lista[i][int(str(id)[i])]
                    for i in range(len(lista))])

def getBuzzWord(col1, col2, col3):
    """Devuelve el buzzword asociado a esas 3 cifras"""
    return generateBuzzWord(''.join([str(col1), str(col2), str(col3)]))

def showAllBuzzword():
    """Muestra todos los buzzwords"""
    return [generateBuzzWord(y) for y in [str(x).zfill(3) for x in range(1000)]]

print('Todas las palabras ', len(showAllBuzzword()))
print('Generamos buzzword aleatoria ', generateRandomBuzzWord())
print('Generamos buzzword con numeros entre 0 y 999 ', generateBuzzWord('042'))
print('Generamos buzzword con tres digitos por separado ', getBuzzWord(0,4,2))