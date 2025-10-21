# operaciones.py

class MiClase:
    """Esta es una clase de ejemplo."""

    pass

def suma(a, b):
    """
    Esto es un comentario de varias líneas
    que explica que esta función realiza
    la suma de dos números.
    """
    return a + b


def resta(a, b):
    """
    Esto es un comentraio de varias líneas
    que explica que esta función realiza
    la suma de dos números.
    """
    return a - b


def multiplicacion(a, b):
    """
    Esto es otro comentario de varias líneas
    que explica que esta función realiza
    la multiplicación de dos números.
    """
    return a * b


def division(a, b):
    """
    Esto es otro comentario de varias líneas
    que explica que esta función realiza
    la división de dos números.
    """
    if b != 0:
        return a / b
    else:
        return "Error: División por cero"
