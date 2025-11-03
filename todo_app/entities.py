from dataclasses import dataclass, field
from enum import Enum

class Prioridad(Enum):
    ALTA = "alta"
    MEDIA = "media"
    BAJA = "baja"

@dataclass
class Categoria:
    principal: str = field(metadata={"max_length": 20})
    sub: str = field(metadata={"max_length": 20})

    def __init__(self, principal, sub):
        self.principal = principal
        self.sub = sub

    def __str__(self):
        return (f"""
           Categoría: {self.principal}
           Subcategoria: {self.sub}
                """)

@dataclass
class Tarea:
    id: int
    descripcion: str = field(metadata={"max_length": 20})
    prioridad: Prioridad
    completada: bool
    categoria: Categoria

    def __init__(self, id, descripcion, prioridad, completada, categoria):
        self.id = id
        self.descripcion = descripcion
        self.prioridad = prioridad
        if isinstance(categoria, dict):
            self.categoria = Categoria(**categoria) # = Categoria(principal=categoria['principal'], sub=categoria['sub'])
        else:
            self.categoria = categoria
        self.completada = completada

    def to_json(self):
        """Crea un diccionario con la clase Tarea."""
        return {
            "id": self.id,
            "descripcion": self.descripcion,
            "prioridad": self.prioridad.value,
            "completada": self.completada,
            "categoria": {
                "principal": self.categoria.principal,
                "sub": self.categoria.sub,
            }
        }

    @classmethod
    def from_json(cls, data):
        """Crea una instancia de Tarea a partir de un diccionario."""
        return cls(data['id'],
                   data['descripcion'],
                   Prioridad(data['prioridad']),
                   data['completada'],
                   data['categoria'])

    def __str__(self):
        return (f"""
           ID: {self.id}
           Descripción: {self.descripcion}
           Prioridad: {self.prioridad}
           Categoría: {self.categoria.principal} / {self.categoria.sub}
           Estado: {"Completada" if self.completada else "Pendiente"}
                """)