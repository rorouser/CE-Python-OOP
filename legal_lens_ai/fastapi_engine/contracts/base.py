"""
Clase base abstracta para contratos auditables.

Aplica el patron Template Method: define el flujo (`audit`) y delega en las
subclases la parte especifica (marco legal, banderas rojas tipicas, datos clave).
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Literal

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Schemas compartidos por todas las subclases
# ---------------------------------------------------------------------------
Severity = Literal["ALTA", "MEDIA", "BAJA"]


class RedFlag(BaseModel):
    """Una clausula problematica detectada por el agente."""
    clausula: str = Field(..., description="Nombre o resumen corto de la clausula")
    problema: str = Field(..., description="Por que es problematica o ilegal")
    articulo_legal: str = Field(
        default="",
        description="Articulo o ley vulnerada (ej: 'LAU art. 9', 'Ley 1/2019 art. 1')",
    )
    severidad: Severity = "MEDIA"


class AuditResult(BaseModel):
    """Resultado completo de la auditoria de un contrato."""
    contract_type: str
    summary: str = Field(..., description="Resumen ejecutivo en 2-3 frases")
    key_data: dict = Field(default_factory=dict, description="Datos clave extraidos")
    red_flags: list[RedFlag] = Field(default_factory=list)
    is_clean: bool = Field(..., description="True si no hay banderas rojas")


# ---------------------------------------------------------------------------
# BaseContract
# ---------------------------------------------------------------------------
class BaseContract(ABC):
    """
    Contrato auditable. Las subclases deben definir:
      - CONTRACT_TYPE: identificador legible
      - LEGAL_FRAMEWORK: texto del marco legal aplicable
      - TYPICAL_RED_FLAGS: lista de patrones tipicos a buscar
      - KEY_DATA_FIELDS: campos a extraer (firmantes, fechas, importes...)
    """

    CONTRACT_TYPE: str = ""
    LEGAL_FRAMEWORK: str = ""
    TYPICAL_RED_FLAGS: list[str] = []
    KEY_DATA_FIELDS: list[str] = []

    def __init__(self, text: str):
        self.text = text

    # --- Template Method ----------------------------------------------------
    def build_audit_prompt(self) -> str:
        """Compone el prompt especifico para este tipo de contrato."""
        red_flags_block = "\n".join(f"  - {rf}" for rf in self.TYPICAL_RED_FLAGS)
        key_fields_block = ", ".join(self.KEY_DATA_FIELDS)
        return (
            f"Eres un abogado especialista en {self.CONTRACT_TYPE} con 20 anos de "
            f"experiencia en derecho espanol.\n\n"
            f"=== MARCO LEGAL APLICABLE ===\n{self.LEGAL_FRAMEWORK}\n\n"
            f"=== BANDERAS ROJAS TIPICAS A BUSCAR ===\n{red_flags_block}\n\n"
            f"=== DATOS CLAVE A EXTRAER ===\n{key_fields_block}\n\n"
            f"=== INSTRUCCIONES ===\n"
            f"1. Lee el contrato completo.\n"
            f"2. Extrae los datos clave (key_data) como diccionario plano.\n"
            f"3. Detecta TODAS las clausulas abusivas, ilegales o desfavorables. "
            f"Para cada una indica: clausula, problema, articulo_legal, severidad "
            f"(ALTA/MEDIA/BAJA).\n"
            f"4. Genera un summary ejecutivo de 2-3 frases.\n"
            f"5. Marca is_clean=true SOLO si NO encuentras ninguna bandera roja.\n"
            f"6. Si una clausula es legal pero perjudicial, sigue siendo bandera roja "
            f"con severidad MEDIA o BAJA.\n"
        )

    @property
    @abstractmethod
    def display_name(self) -> str:
        """Nombre humano del tipo de contrato (para logs/UI)."""
