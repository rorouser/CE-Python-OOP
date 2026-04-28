"""Contrato de arrendamiento de vivienda - Ley de Arrendamientos Urbanos (LAU)."""
from __future__ import annotations

from .base import BaseContract


class RentalContract(BaseContract):
    CONTRACT_TYPE = "contrato de arrendamiento de vivienda"
    LEGAL_FRAMEWORK = """
Ley 29/1994 de Arrendamientos Urbanos (LAU), modificada por RDL 7/2019:
  - Art. 9: duracion minima del arrendamiento de vivienda habitual: 5 anos
    (7 si el arrendador es persona juridica). Prorroga obligatoria para el inquilino.
  - Art. 18: actualizacion de la renta: solo permitida una vez al ano y nunca
    superior al IPC (o IRAV en zonas tensionadas). Subidas semestrales o
    superiores al IPC son nulas.
  - Art. 36: fianza obligatoria de 1 mensualidad, depositada en el organismo
    autonomico competente. Garantias adicionales: maximo 2 mensualidades extra.
  - Art. 20: gastos generales (IBI, comunidad) repercutibles solo si se pacta
    expresamente y por escrito.
  - Codigo Civil art. 1255: limite de la autonomia de la voluntad - no caben
    pactos contra la ley, la moral o el orden publico.
  - LEC art. 52: la jurisdiccion competente es la del lugar del inmueble. Pactos
    de sumision a tribunales extranjeros en arrendamientos sobre suelo espanol
    son nulos.
""".strip()

    TYPICAL_RED_FLAGS = [
        "Fianza superior a 1 mensualidad sin justificacion legal",
        "Fianza no depositada en organismo oficial (IVIMA, AVS, etc.)",
        "Duracion menor de 5 anos sin renovacion obligatoria",
        "Renuncia del inquilino a la prorroga legal",
        "Subidas de renta superiores al IPC",
        "Subidas de renta con periodicidad inferior a 1 ano",
        "Repercusion al inquilino de IBI o comunidad sin pacto explicito",
        "Penalizaciones desproporcionadas por desistimiento",
        "Sumision a jurisdiccion extranjera o no espanola",
        "Prohibiciones absolutas de empadronamiento o convivencia",
        "Clausulas de desahucio express extrajudicial",
    ]

    KEY_DATA_FIELDS = [
        "propietario", "dni_propietario",
        "inquilino", "dni_inquilino",
        "direccion_inmueble",
        "renta_mensual",
        "fianza",
        "duracion",
        "fecha_inicio",
        "jurisdiccion",
    ]

    @property
    def display_name(self) -> str:
        return "Arrendamiento de vivienda"
