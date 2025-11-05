from dataclasses import dataclass, field
from enum import Enum

class Prioridad(Enum):
    ALTA = "alta"
    MEDIA = "media"
    BAJA = "baja"

@dataclass
class Categoria:
    _principal: str = field(metadata={"max_length": 20})
    _sub: str = field(metadata={"max_length": 20})

    def __init__(self, principal, sub):
        self.principal = principal
        self.sub = sub

    @property
    def principal(self):
        return self._principal

    @principal.setter
    def principal(self, principal):
        if isinstance(principal, str):
            self._principal = principal

    @property
    def sub(self):
        return self._sub

    @sub.setter
    def sub(self, sub):
        if isinstance(sub, str):
            self._sub = sub

    def __str__(self):
        return (f"""
           Categoría: {self.principal}
           Subcategoria: {self.sub}
                """)

@dataclass
class Tarea:
    _id: int
    _descripcion: str = field(metadata={"max_length": 20})
    _prioridad: Prioridad
    _completada: bool
    _categoria: Categoria

    def __init__(self, id, descripcion, prioridad, completada, categoria):
        self._id = id
        self._descripcion = descripcion
        self._prioridad = prioridad
        if isinstance(categoria, dict):
            self._categoria = Categoria(**categoria) # = Categoria(principal=categoria['principal'], sub=categoria['sub'])
        else:
            self._categoria = categoria
        self._completada = completada

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        if isinstance(id, int):
            self._id = id

    @property
    def descripcion(self):
        return self._descripcion

    @descripcion.setter
    def descripcion(self, descripcion):
        if isinstance(descripcion, str):
            self._descripcion = descripcion

    @property
    def prioridad(self):
        return self._prioridad

    @prioridad.setter
    def prioridad(self, prioridad):
        if isinstance(prioridad, Prioridad):
            self._prioridad = prioridad

    @property
    def completada(self):
        return self._completada

    @completada.setter
    def completada(self, completada):
        if isinstance(completada, bool):
            self._completada = completada

    @property
    def categoria(self):
        return self._categoria

    @categoria.setter
    def categoria(self, categoria):
        if isinstance(categoria, Categoria):
            self._categoria = categoria


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