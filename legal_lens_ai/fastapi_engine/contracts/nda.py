"""Contrato de confidencialidad (NDA) - Ley 1/2019 de Secretos Empresariales."""
from __future__ import annotations

from .base import BaseContract


class NDAContract(BaseContract):
    CONTRACT_TYPE = "contrato de confidencialidad (NDA)"
    LEGAL_FRAMEWORK = """
Ley 1/2019 de Secretos Empresariales y normativa concordante:
  - Art. 1: define secreto empresarial. La proteccion exige que la informacion
    sea secreta, tenga valor comercial y se hayan adoptado medidas razonables
    para mantenerla confidencial.
  - Plazo razonable de confidencialidad: tipicamente 3-5 anos para informacion
    no critica. Plazos perpetuos son desproporcionados salvo para secretos
    industriales muy especificos y suelen considerarse abusivos.
  - Codigo Civil art. 1255 y 1258: principio de buena fe y limites a la
    autonomia de la voluntad. Penalizaciones desorbitadas pueden moderarse
    judicialmente (art. 1154 CC).
  - Estatuto de los Trabajadores art. 21: pacto de no competencia post-contractual:
    duracion maxima 2 anos para tecnicos, 6 meses para otros, exige compensacion
    economica adecuada e interes industrial o comercial efectivo.
  - LOPDGDD y RGPD: tratamiento de datos personales debe respetar la normativa
    de proteccion de datos.
  - LOPJ art. 22: jurisdiccion espanola exclusiva en ciertas materias. Sumision
    a tribunales extranjeros (Cayman, Singapur, etc.) sin conexion real con la
    operacion suele considerarse abusiva.
""".strip()

    TYPICAL_RED_FLAGS = [
        "Confidencialidad perpetua o por mas de 10 anos sin justificacion",
        "Definicion de informacion confidencial ambigua o demasiado amplia",
        "Ausencia de excepciones (informacion publica, requerida por ley, etc.)",
        "Penalizaciones economicas desorbitadas sin posibilidad de moderacion",
        "Pacto de no competencia superior a 2 anos sin compensacion economica",
        "Sumision a jurisdiccion extranjera sin conexion con la operacion",
        "Renuncia al derecho de tutela judicial efectiva",
        "Obligaciones unilaterales (solo una parte queda obligada)",
        "Cesion automatica de propiedad intelectual sin contraprestacion",
        "Clausulas de auditoria invasivas y desproporcionadas",
    ]

    KEY_DATA_FIELDS = [
        "parte_reveladora", "cif_parte_reveladora",
        "parte_receptora", "cif_parte_receptora",
        "objeto",
        "duracion_confidencialidad",
        "duracion_no_competencia",
        "penalizacion",
        "jurisdiccion",
        "fecha_firma",
    ]

    @property
    def display_name(self) -> str:
        return "Acuerdo de confidencialidad (NDA)"
