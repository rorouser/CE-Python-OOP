"""
Jerarquia POO de contratos: BaseContract -> RentalContract / NDAContract.

Cada subclase aporta:
  - el marco legal aplicable (texto inyectado en el prompt del agente)
  - la lista de banderas rojas tipicas a buscar
  - la estructura de datos clave a extraer
"""
from .base import BaseContract, RedFlag, AuditResult
from .rental import RentalContract
from .nda import NDAContract


def get_contract(contract_type: str, text: str) -> BaseContract:
    """Factory: instancia la subclase adecuada segun el tipo."""
    t = (contract_type or "").upper().strip()
    if t == "RENTAL":
        return RentalContract(text)
    if t == "NDA":
        return NDAContract(text)
    raise ValueError(f"Tipo de contrato no soportado: {contract_type!r}")


__all__ = [
    "BaseContract",
    "RentalContract",
    "NDAContract",
    "RedFlag",
    "AuditResult",
    "get_contract",
]
