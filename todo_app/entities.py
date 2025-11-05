from dataclasses import dataclass, field
from enum import Enum

class Prioridad(Enum):
    ALTA = "Alta"
    MEDIA = "Media"
    BAJA = "Baja"

class CategoriaPrincipal(Enum):
    TRABAJO = "Trabajo"
    PERSONAL = "Personal"
    ESTUDIO = "Estudio"
    OTROS = "Otros"

class Subcategoria(Enum):
    pass

class SubcategoriaTrabajo(Subcategoria):
    REUNIONES = "Reuniones"
    LLAMADAS = "Llamadas"
    PROYECTOS = "Proyectos"

class SubcategoriaPersonal(Subcategoria):
    FINANZAS = "Finanzas"
    SALUD = "Salud"
    HOGAR = "Hogar"

class SubcategoriaEstudio(Subcategoria):
    EXAMENES = "Examenes"
    TAREAS = "Tareas"
    LECTURAS = "Lecturas"

SUBCATEGORIAS_POR_CATEGORIA = {
    CategoriaPrincipal.TRABAJO: SubcategoriaTrabajo,
    CategoriaPrincipal.PERSONAL: SubcategoriaPersonal,
    CategoriaPrincipal.ESTUDIO: SubcategoriaEstudio
}

@dataclass
class Categoria:
    _principal: CategoriaPrincipal
    _sub: Enum  # puede ser cualquiera de los enums de subcategoría

    def __init__(self, principal, sub):
        # Permitir strings o Enums
        if isinstance(principal, str):
            principal = CategoriaPrincipal(principal.capitalize())

        sub_enum_cls = SUBCATEGORIAS_POR_CATEGORIA.get(principal)

        if sub_enum_cls is None:
            raise ValueError(f"No hay subcategorías definidas para la categoría {principal.value}")

        # Permitir strings para subcategoría
        if isinstance(sub, str):
            # Buscar en el Enum correspondiente
            try:
                sub = next(s for s in sub_enum_cls if s.value.lower() == sub.lower())
            except StopIteration:
                raise ValueError(
                    f"La subcategoría '{sub}' no pertenece a '{principal.value}'. "
                    f"Opciones válidas: {[s.value for s in sub_enum_cls]}"
                )

        # Validar que el sub sea del Enum correcto
        if not isinstance(sub, sub_enum_cls):
            raise ValueError(
                f"La subcategoría '{sub}' no pertenece a la categoría '{principal.value}'."
            )

        self._principal = principal
        self._sub = sub

    @property
    def principal(self):
        return self._principal

    @principal.setter
    def principal(self, principal):
        if isinstance(principal, CategoriaPrincipal):
            self._principal = principal

    @property
    def sub(self):
        return self._sub

    @sub.setter
    def sub(self, sub):
        if isinstance(sub, Subcategoria):
            self._sub = sub

    def __str__(self):
        return f"Categoría: {self.principal.value} / {self.sub.value}"

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
                "principal": self.categoria.principal.value,
                "sub": self.categoria.sub.value
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
           Prioridad: {self.prioridad.value}
           Categoría: {self.categoria.principal.value} / {self.categoria.sub.value}
           Estado: {"Completada" if self.completada else "Pendiente"}
                """)