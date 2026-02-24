from pydantic import BaseModel, field_validator
from datetime import datetime


class RecintoBase(BaseModel):
    nombre: str
    ciudad: str
    capacidad: int


class RecintoCreate(RecintoBase):
    pass


class RecintoUpdate(RecintoBase):
    pass


class RecintoOut(RecintoBase):
    id: int

    class Config:
        from_attributes = True


class EventoBase(BaseModel):
    nombre: str
    fecha: datetime
    precio: float
    recinto_id: int

    @field_validator("precio")
    @classmethod
    def precio_no_negativo(cls, v):
        if v < 0:
            raise ValueError("El precio no puede ser negativo")
        return v


class EventoCreate(EventoBase):
    pass


class EventoUpdate(EventoBase):
    pass


class EventoOut(EventoBase):
    id: int
    tickets_vendidos: int
    recinto: RecintoOut

    class Config:
        from_attributes = True

class CompraIn(BaseModel):
    cantidad: int
