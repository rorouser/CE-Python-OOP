from typing import Optional, List
from pydantic import BaseModel, Field, field_validator

from app.models import ScooterStatus


class ZoneCreate(BaseModel):
    nombre: str
    codigo_postal: str
    limite_velocidad: int


class ZoneRead(ZoneCreate):
    id: int

    model_config = {"from_attributes": True}


class ScooterCreate(BaseModel):
    numero_serie: str
    modelo: str
    bateria: float = Field(..., ge=0, le=100, description="Nivel de batería entre 0 y 100")
    estado: ScooterStatus = ScooterStatus.disponible
    zona_id: int
    puntuacion_usuario: Optional[float] = None

    @field_validator("bateria")
    @classmethod
    def bateria_range(cls, v: float) -> float:
        if v < 0 or v > 100:
            raise ValueError("La batería debe estar entre 0 y 100")
        return v


class ScooterRead(ScooterCreate):
    id: int

    model_config = {"from_attributes": True}


class MantenimientoResponse(BaseModel):
    zona_id: int
    patinetes_actualizados: int
    mensaje: str
