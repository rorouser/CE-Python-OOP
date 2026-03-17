import enum
from sqlalchemy import Column, Integer, String, Float, Enum, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class ScooterStatus(str, enum.Enum):
    disponible = "disponible"
    en_uso = "en_uso"
    mantenimiento = "mantenimiento"
    sin_bateria = "sin_bateria"


class Zone(Base):
    __tablename__ = "zones"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    codigo_postal = Column(String, nullable=False)
    limite_velocidad = Column(Integer, nullable=False)

    patinetes = relationship("Scooter", back_populates="zona")


class Scooter(Base):
    __tablename__ = "scooters"

    id = Column(Integer, primary_key=True, index=True)
    numero_serie = Column(String, unique=True, nullable=False, index=True)
    modelo = Column(String, nullable=False)
    bateria = Column(Float, nullable=False)
    estado = Column(Enum(ScooterStatus), nullable=False, default=ScooterStatus.disponible)
    zona_id = Column(Integer, ForeignKey("zones.id"), nullable=False)


    zona = relationship("Zone", back_populates="patinetes")
