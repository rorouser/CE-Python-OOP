from dataclasses import dataclass, field
from enum import Enum

class Prioridad(Enum):
    ALTA = "Alta"
    MEDIA = "Media"
    BAJA = "Baja"

@dataclass
class Categoria:
    principal: str = field(metadata={"max_length": 20})
    sub: str = field(metadata={"max_length": 20})

@dataclass
class Tarea:
    id: int
    descripcion: str = field(metadata={"max_length": 20})
    prioridad: Prioridad
    completada: bool
    categoria: Categoria
