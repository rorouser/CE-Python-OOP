class Jugador:
    def __init__(self, dni, nombre, posicion, altura):
        self.nombre = nombre
        self.dni = dni
        self.posicion = posicion
        self.altura = altura

    def __str__(self):
        return f"Jugador(dni='{self.dni}', nombre={self.nombre}, posicion={self.posicion}, altura={self.altura})"

def altaJugador(plantilla, dorsal):
    """que añade una entrada al
    diccionario con el dorsal y el jugador creado dentro del
    método, introduciendo sus datos por consola."""

    dni = input("Digite el DNI: ")
    nombre = input("Digite el nombre: ")
    posicion = input("Digite el posicion: ")
    altura = input("Digite la altura: ")
    if dorsal not in plantilla.keys():
        plantilla[dorsal] = Jugador(dni, nombre, posicion, altura)
    else:
        print("El dorsal {} ya existe!".format(dorsal))


def eliminarJugador(plantilla, dorsal):
    """que elimina la entrada
    correspondiente al jugador. Dicho dorsal desaparece del
    diccionario hasta que se asigne a otro jugador por medio de un
    alta. El método devuelve el jugador eliminado."""
    if dorsal in plantilla.keys():
        del plantilla[dorsal]
    else:
        print("El dorsal {} no existe!".format(dorsal))

def mostrar (plantilla):
    """que muestra una lista de los dorsales
    con los nombres de los jugadores correspondientes."""
    [print(v,k) for v, k in plantilla.items()]

def editarJugador(plantilla, dorsal):
    """que permite modificar los
    datos de un jugador, excepto su dorsal y su DNI. Devuelve true
    si el dorsal existe y false en caso contrario. ¡¡ HAY que Cambiar el jugador uno por otro no lo que pone en el enynciado!!"""
    dni = input("Digite el DNI: ")
    nombre = input("Digite el nombre: ")
    posicion = input("Digite el posicion: ")
    altura = input("Digite la altura: ")
    if dorsal in plantilla.keys():
        plantilla[dorsal] = Jugador(dni, nombre, posicion, altura)
    else:
        print("El dorsal {} no existe!".format(dorsal))

# Programa principal
j1 = Jugador("28548847", "SERGIO", "CENTROCAMPISTA", 160)
j2 = Jugador("28544447", "ANDRES", "DELANTERO", 180)
j3 = Jugador("23338847", "SULI", "DELANTERO", 190)
j4 = Jugador("28511147", "JONATAN", "DEFENSA", 165)
j5 = Jugador("28523237", "LUIS", "CENTROCAMPISTA", 160)
# alta de varios jugadores
plantilla = {6: j1, 5: j2, 7: j3, 2: j4, 3: j5}
print("PLANTILLA ACTUAL ..................")
mostrar(plantilla)
print("Alta del jugador con el dorsal 10 ..........")
altaJugador(plantilla, 10)
print("Elimina al jugador con el dorsal 7 ..........")
eliminarJugador(plantilla, 7)
print("PLANTILLA ACTUAL ..................")
mostrar(plantilla)
print("Edita al jugador con el dorsal 2 ..........")
editarJugador(plantilla, 2)
print("PLANTILLA ACTUAL ..................")
mostrar(plantilla)