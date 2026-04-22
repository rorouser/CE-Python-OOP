"""
Generador de 4 PDFs de muestra para LegalLens AI:
  1. Contrato de alquiler CORRECTO (cumple LAU)
  2. Contrato de alquiler INCORRECTO (con cláusulas abusivas/ilegales)
  3. NDA CORRECTO (acuerdo de confidencialidad valido)
  4. NDA INCORRECTO (con cláusulas abusivas)

Salida: legal_lens_ai/sample_pdfs/*.pdf
"""

import os
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak
)


SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "sample_pdfs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# -----------------------------------------------------------------------------
# Helpers de estilo
# -----------------------------------------------------------------------------
def get_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="LegalTitle",
        parent=styles["Title"],
        fontSize=16,
        spaceAfter=20,
        alignment=TA_CENTER,
    ))
    styles.add(ParagraphStyle(
        name="LegalH2",
        parent=styles["Heading2"],
        fontSize=12,
        spaceBefore=12,
        spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        name="LegalBody",
        parent=styles["BodyText"],
        fontSize=10.5,
        leading=14,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
    ))
    return styles


def build_pdf(filename: str, blocks):
    """blocks: lista de tuplas (style_name, texto)."""
    styles = get_styles()
    doc = SimpleDocTemplate(
        str(OUTPUT_DIR / filename),
        pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm,
    )
    story = []
    for style_name, text in blocks:
        if style_name == "PAGEBREAK":
            story.append(PageBreak())
        elif style_name == "SPACER":
            story.append(Spacer(1, 0.4 * cm))
        else:
            story.append(Paragraph(text, styles[style_name]))
    doc.build(story)
    print(f"OK -> {filename}")


# -----------------------------------------------------------------------------
# 1) CONTRATO DE ALQUILER CORRECTO (cumple LAU)
# -----------------------------------------------------------------------------
def alquiler_correcto():
    blocks = [
        ("LegalTitle", "CONTRATO DE ARRENDAMIENTO DE VIVIENDA HABITUAL"),
        ("LegalBody", "En Madrid, a 15 de marzo de 2025."),
        ("LegalH2", "REUNIDOS"),
        ("LegalBody",
         "DE UNA PARTE, D. Carlos Martínez Ruiz, mayor de edad, "
         "con DNI 12345678-A, y domicilio en calle Mayor 23, 28001 Madrid, "
         "en adelante, el ARRENDADOR."),
        ("LegalBody",
         "DE OTRA PARTE, Dña. Laura Sánchez Gómez, mayor de edad, "
         "con DNI 87654321-B, y domicilio en calle Goya 45, 28009 Madrid, "
         "en adelante, la ARRENDATARIA."),
        ("LegalH2", "EXPONEN"),
        ("LegalBody",
         "Que el ARRENDADOR es propietario de la vivienda situada en "
         "calle Alcalá 100, 4º Izquierda, 28009 Madrid, "
         "con referencia catastral 1234567VK4713S0001ZZ, "
         "que destinará a vivienda habitual de la ARRENDATARIA."),
        ("LegalH2", "CLÁUSULAS"),
        ("LegalH2", "PRIMERA. - Objeto y destino"),
        ("LegalBody",
         "El ARRENDADOR cede en arrendamiento a la ARRENDATARIA la vivienda "
         "descrita, que se destinará exclusivamente a vivienda habitual y "
         "permanente de la misma, conforme al artículo 2 de la Ley 29/1994, "
         "de 24 de noviembre, de Arrendamientos Urbanos (LAU)."),
        ("LegalH2", "SEGUNDA. - Duración"),
        ("LegalBody",
         "El presente contrato tendrá una duración inicial de UN AÑO, "
         "que se prorrogará obligatoriamente por plazos anuales hasta alcanzar "
         "los CINCO AÑOS, conforme al artículo 9 de la LAU. "
         "La ARRENDATARIA podrá desistir del contrato transcurridos seis meses, "
         "comunicándolo al ARRENDADOR con treinta días de antelación."),
        ("LegalH2", "TERCERA. - Renta"),
        ("LegalBody",
         "La renta mensual pactada es de NOVECIENTOS EUROS (900,00 €), "
         "que se abonarán mediante transferencia bancaria en la cuenta "
         "ES12 3456 7890 1234 5678 9012, dentro de los siete primeros días "
         "de cada mes."),
        ("LegalH2", "CUARTA. - Actualización de la renta"),
        ("LegalBody",
         "La renta se actualizará anualmente conforme a la variación del "
         "Índice de Garantía de Competitividad (IGC) o, en su defecto, "
         "conforme al Índice de Precios al Consumo (IPC) publicado por el INE, "
         "respetando los límites que establezca la legislación vigente."),
        ("LegalH2", "QUINTA. - Fianza"),
        ("LegalBody",
         "A la firma del presente contrato, la ARRENDATARIA entrega al "
         "ARRENDADOR la cantidad de NOVECIENTOS EUROS (900,00 €), "
         "equivalente a UNA mensualidad de renta, en concepto de fianza "
         "legal, conforme al artículo 36 de la LAU. "
         "Dicha fianza será depositada por el ARRENDADOR ante el organismo "
         "competente de la Comunidad de Madrid."),
        ("LegalH2", "SEXTA. - Conservación y reparaciones"),
        ("LegalBody",
         "Las reparaciones necesarias para conservar la vivienda en condiciones "
         "de habitabilidad correrán a cargo del ARRENDADOR, salvo aquellas "
         "derivadas del desgaste por uso ordinario de la vivienda, "
         "conforme al artículo 21 de la LAU."),
        ("LegalH2", "SÉPTIMA. - Obras"),
        ("LegalBody",
         "La ARRENDATARIA no podrá realizar obras que modifiquen la "
         "configuración de la vivienda sin autorización escrita del "
         "ARRENDADOR, conforme al artículo 23 de la LAU."),
        ("LegalH2", "OCTAVA. - Cesión y subarriendo"),
        ("LegalBody",
         "La cesión del contrato y el subarriendo total o parcial requerirán "
         "consentimiento expreso y por escrito del ARRENDADOR, "
         "conforme al artículo 8 de la LAU."),
        ("LegalH2", "NOVENA. - Jurisdicción"),
        ("LegalBody",
         "Para la resolución de cuantas controversias pudieran derivarse del "
         "presente contrato, las partes se someten a los Juzgados y Tribunales "
         "de Madrid, sin perjuicio del fuero del consumidor cuando resulte aplicable."),
        ("SPACER", ""),
        ("LegalBody",
         "Y en prueba de conformidad, las partes firman el presente contrato "
         "por duplicado y a un solo efecto en el lugar y fecha indicados."),
        ("SPACER", ""),
        ("LegalBody", "EL ARRENDADOR<br/><br/>Fdo. Carlos Martínez Ruiz"),
        ("SPACER", ""),
        ("LegalBody", "LA ARRENDATARIA<br/><br/>Fdo. Laura Sánchez Gómez"),
    ]
    build_pdf("contrato_alquiler_correcto.pdf", blocks)


# -----------------------------------------------------------------------------
# 2) CONTRATO DE ALQUILER INCORRECTO (con clausulas abusivas)
# -----------------------------------------------------------------------------
def alquiler_incorrecto():
    blocks = [
        ("LegalTitle", "CONTRATO DE ARRENDAMIENTO DE VIVIENDA"),
        ("LegalBody", "En Barcelona, a 5 de abril de 2025."),
        ("LegalH2", "REUNIDOS"),
        ("LegalBody",
         "De una parte, D. Roberto Vega Iglesias, con DNI 11223344-X, "
         "en adelante el PROPIETARIO."),
        ("LegalBody",
         "De otra parte, D. Andrés Romero López, con DNI 99887766-Y, "
         "en adelante el INQUILINO."),
        ("LegalH2", "CLÁUSULAS"),
        ("LegalH2", "PRIMERA. - Objeto"),
        ("LegalBody",
         "Se arrienda la vivienda sita en Av. Diagonal 250, 3º A, Barcelona, "
         "para uso de vivienda."),
        ("LegalH2", "SEGUNDA. - Duración"),
        ("LegalBody",
         "El contrato tendrá una duración improrrogable de SEIS MESES, "
         "tras los cuales el INQUILINO deberá abandonar la vivienda sin "
         "derecho a prórroga ni a indemnización alguna. "
         "El INQUILINO renuncia expresamente al derecho de prórroga "
         "obligatoria establecido en la LAU."),
        ("LegalH2", "TERCERA. - Renta"),
        ("LegalBody",
         "La renta mensual será de MIL DOSCIENTOS EUROS (1.200,00 €), "
         "pagaderos por adelantado el día 1 de cada mes. "
         "El retraso de un solo día en el pago supondrá una penalización "
         "del 20% sobre la mensualidad y facultará al PROPIETARIO a "
         "resolver el contrato de forma inmediata sin necesidad de "
         "requerimiento judicial."),
        ("LegalH2", "CUARTA. - Actualización"),
        ("LegalBody",
         "La renta se incrementará automáticamente cada seis meses en un 8%, "
         "independientemente del IPC o de cualquier otro índice oficial."),
        ("LegalH2", "QUINTA. - Fianza y garantías"),
        ("LegalBody",
         "El INQUILINO entrega en este acto la cantidad de SEIS MIL EUROS "
         "(6.000,00 €), equivalente a CINCO mensualidades, en concepto de "
         "fianza. Esta cantidad no será depositada en organismo alguno y "
         "quedará en poder del PROPIETARIO. Adicionalmente, el INQUILINO "
         "deberá entregar dos avales personales solidarios de familiares "
         "directos."),
        ("LegalH2", "SEXTA. - Reparaciones"),
        ("LegalBody",
         "Todas las reparaciones, incluidas las estructurales, las de "
         "fontanería, electricidad, calefacción y cualquier elemento de la "
         "vivienda, serán por cuenta exclusiva del INQUILINO, "
         "independientemente de su origen o causa."),
        ("LegalH2", "SÉPTIMA. - Prohibiciones"),
        ("LegalBody",
         "Queda terminantemente prohibido al INQUILINO empadronarse en la "
         "vivienda, recibir visitas que pernocten, tener animales de "
         "compañía, instalar electrodomésticos adicionales o ausentarse "
         "más de 15 días consecutivos sin autorización escrita."),
        ("LegalH2", "OCTAVA. - Resolución"),
        ("LegalBody",
         "El PROPIETARIO podrá resolver el contrato y exigir el desalojo "
         "inmediato sin necesidad de procedimiento judicial alguno, "
         "pudiendo acceder a la vivienda con sus propias llaves para "
         "verificar el cumplimiento del contrato cuando lo estime oportuno."),
        ("LegalH2", "NOVENA. - Renuncia de derechos"),
        ("LegalBody",
         "El INQUILINO renuncia expresamente a cualquier derecho que pudiera "
         "corresponderle como consumidor, así como al derecho de tanteo y "
         "retracto en caso de venta de la vivienda."),
        ("LegalH2", "DÉCIMA. - Jurisdicción"),
        ("LegalBody",
         "Las partes se someten a los Tribunales de Andorra la Vella, "
         "renunciando expresamente al fuero que pudiera corresponderles."),
        ("SPACER", ""),
        ("LegalBody", "EL PROPIETARIO<br/><br/>Fdo. Roberto Vega Iglesias"),
        ("SPACER", ""),
        ("LegalBody", "EL INQUILINO<br/><br/>Fdo. Andrés Romero López"),
    ]
    build_pdf("contrato_alquiler_incorrecto.pdf", blocks)


# -----------------------------------------------------------------------------
# 3) NDA CORRECTO
# -----------------------------------------------------------------------------
def nda_correcto():
    blocks = [
        ("LegalTitle", "ACUERDO DE CONFIDENCIALIDAD (NDA)"),
        ("LegalBody", "En Valencia, a 10 de febrero de 2025."),
        ("LegalH2", "REUNIDOS"),
        ("LegalBody",
         "DE UNA PARTE, TECH SOLUTIONS S.L., con CIF B-12345678, "
         "domicilio social en calle Colón 35, 46004 Valencia, "
         "representada por D. Javier Ortiz Pérez, con DNI 23456789-C, "
         "en adelante, la PARTE REVELADORA."),
        ("LegalBody",
         "DE OTRA PARTE, INNOVA CONSULTING S.L., con CIF B-87654321, "
         "domicilio social en calle Xátiva 10, 46002 Valencia, "
         "representada por Dña. María Castro Vidal, con DNI 34567890-D, "
         "en adelante, la PARTE RECEPTORA."),
        ("LegalH2", "EXPONEN"),
        ("LegalBody",
         "Que las partes se encuentran en negociaciones para la posible "
         "colaboración en el desarrollo de un proyecto de software "
         "empresarial, en cuyo marco la PARTE REVELADORA podrá compartir "
         "información confidencial con la PARTE RECEPTORA."),
        ("LegalH2", "CLÁUSULAS"),
        ("LegalH2", "PRIMERA. - Información Confidencial"),
        ("LegalBody",
         "A efectos del presente acuerdo, se entenderá por Información "
         "Confidencial toda información técnica, comercial, financiera o "
         "estratégica, ya sea oral, escrita o en cualquier otro soporte, "
         "que la PARTE REVELADORA marque expresamente como confidencial "
         "o que, por su naturaleza, deba considerarse como tal."),
        ("LegalH2", "SEGUNDA. - Excepciones"),
        ("LegalBody",
         "No se considerará Información Confidencial aquella que: "
         "(i) sea o llegue a ser de dominio público sin culpa de la PARTE "
         "RECEPTORA; (ii) ya fuera conocida por la PARTE RECEPTORA antes "
         "de su revelación; (iii) sea desarrollada de forma independiente "
         "por la PARTE RECEPTORA sin uso de la información confidencial; "
         "(iv) sea revelada por mandato legal o judicial, en cuyo caso la "
         "PARTE RECEPTORA notificará inmediatamente a la PARTE REVELADORA."),
        ("LegalH2", "TERCERA. - Obligaciones"),
        ("LegalBody",
         "La PARTE RECEPTORA se compromete a: (a) mantener la Información "
         "Confidencial en secreto, aplicando al menos el mismo nivel de "
         "diligencia que aplica a su propia información confidencial; "
         "(b) no utilizar la información para fines distintos al objeto "
         "del presente acuerdo; (c) limitar el acceso a aquellos empleados "
         "que la necesiten estrictamente, los cuales quedarán igualmente "
         "obligados."),
        ("LegalH2", "CUARTA. - Duración"),
        ("LegalBody",
         "Las obligaciones de confidencialidad establecidas en el presente "
         "acuerdo tendrán una vigencia de TRES (3) AÑOS desde la fecha de "
         "su firma. Transcurrido dicho plazo, las partes quedarán "
         "liberadas de las mismas, salvo respecto de información que "
         "constituya secreto empresarial conforme a la Ley 1/2019, "
         "que se regirá por dicha norma."),
        ("LegalH2", "QUINTA. - Devolución de información"),
        ("LegalBody",
         "A la finalización del acuerdo, o a requerimiento de la PARTE "
         "REVELADORA, la PARTE RECEPTORA devolverá o destruirá toda la "
         "Información Confidencial recibida, certificándolo por escrito."),
        ("LegalH2", "SEXTA. - Incumplimiento"),
        ("LegalBody",
         "El incumplimiento de las obligaciones aquí establecidas dará "
         "derecho a la parte perjudicada a reclamar los daños y perjuicios "
         "efectivamente acreditados, conforme a las reglas generales del "
         "Código Civil."),
        ("LegalH2", "SÉPTIMA. - Ley aplicable y jurisdicción"),
        ("LegalBody",
         "El presente acuerdo se rige por la legislación española. "
         "Para la resolución de cualquier controversia, las partes se "
         "someten a los Juzgados y Tribunales de Valencia."),
        ("SPACER", ""),
        ("LegalBody",
         "PARTE REVELADORA<br/><br/>Fdo. Javier Ortiz Pérez<br/>"
         "Tech Solutions S.L."),
        ("SPACER", ""),
        ("LegalBody",
         "PARTE RECEPTORA<br/><br/>Fdo. María Castro Vidal<br/>"
         "Innova Consulting S.L."),
    ]
    build_pdf("contrato_nda_correcto.pdf", blocks)


# -----------------------------------------------------------------------------
# 4) NDA INCORRECTO (con clausulas abusivas)
# -----------------------------------------------------------------------------
def nda_incorrecto():
    blocks = [
        ("LegalTitle", "ACUERDO DE CONFIDENCIALIDAD"),
        ("LegalBody", "En Sevilla, a 20 de marzo de 2025."),
        ("LegalH2", "REUNIDOS"),
        ("LegalBody",
         "MEGACORP INTERNATIONAL LTD. (en adelante, la EMPRESA), "
         "y D. Pablo Jiménez Núñez (en adelante, el EMPLEADO)."),
        ("LegalH2", "CLÁUSULAS"),
        ("LegalH2", "PRIMERA. - Objeto"),
        ("LegalBody",
         "El EMPLEADO se compromete a guardar absoluta confidencialidad "
         "sobre cualquier información, dato, conversación, idea, comentario "
         "o circunstancia, sin excepción alguna, que conozca o llegue a "
         "conocer durante o después de su relación con la EMPRESA, "
         "ya sea profesional, social o de cualquier otra índole."),
        ("LegalH2", "SEGUNDA. - Duración"),
        ("LegalBody",
         "Las obligaciones de confidencialidad asumidas por el EMPLEADO "
         "tendrán carácter PERPETUO E INDEFINIDO, manteniendo plena vigencia "
         "incluso tras el fallecimiento del EMPLEADO, extendiéndose a sus "
         "herederos y causahabientes."),
        ("LegalH2", "TERCERA. - No competencia"),
        ("LegalBody",
         "El EMPLEADO no podrá trabajar, colaborar, asesorar ni mantener "
         "ningún tipo de relación profesional con empresas del sector "
         "tecnológico en cualquier país del mundo, durante un período "
         "de DIEZ AÑOS desde la finalización de su relación con la EMPRESA, "
         "sin compensación económica alguna por dicha restricción."),
        ("LegalH2", "CUARTA. - Penalización"),
        ("LegalBody",
         "El incumplimiento, total o parcial, de cualquiera de las "
         "obligaciones aquí establecidas, conllevará una penalización "
         "automática de DOS MILLONES DE EUROS (2.000.000,00 €) por cada "
         "infracción, sin necesidad de acreditar daño alguno y sin "
         "posibilidad de moderación judicial. Esta cantidad será exigible "
         "por la EMPRESA con el solo requerimiento extrajudicial."),
        ("LegalH2", "QUINTA. - Renuncia de derechos"),
        ("LegalBody",
         "El EMPLEADO renuncia expresamente a cualquier derecho de "
         "información, acceso, rectificación o supresión sobre los datos "
         "personales tratados por la EMPRESA, así como a cualquier acción "
         "judicial o extrajudicial frente a la EMPRESA por cualquier causa."),
        ("LegalH2", "SEXTA. - Cesión unilateral"),
        ("LegalBody",
         "La EMPRESA podrá ceder los derechos derivados del presente "
         "acuerdo a cualquier tercero sin necesidad de consentimiento ni "
         "notificación al EMPLEADO. El EMPLEADO no podrá ceder sus "
         "obligaciones bajo ningún concepto."),
        ("LegalH2", "SÉPTIMA. - Excepciones"),
        ("LegalBody",
         "No existirán excepciones a las obligaciones de confidencialidad. "
         "Incluso aunque la información se haga pública o sea conocida por "
         "terceros, el EMPLEADO mantendrá su deber de confidencialidad."),
        ("LegalH2", "OCTAVA. - Ley aplicable y jurisdicción"),
        ("LegalBody",
         "El presente acuerdo se rige por la legislación de las Islas "
         "Caimán. Las partes se someten expresamente a los tribunales "
         "arbitrales de Singapur, renunciando a cualquier otro fuero, "
         "incluido el del consumidor o el del trabajador."),
        ("SPACER", ""),
        ("LegalBody",
         "LA EMPRESA<br/><br/>Fdo. Megacorp International Ltd."),
        ("SPACER", ""),
        ("LegalBody",
         "EL EMPLEADO<br/><br/>Fdo. Pablo Jiménez Núñez"),
    ]
    build_pdf("contrato_nda_incorrecto.pdf", blocks)


# -----------------------------------------------------------------------------
def main():
    print(f"Generando PDFs en: {OUTPUT_DIR}\n")
    alquiler_correcto()
    alquiler_incorrecto()
    nda_correcto()
    nda_incorrecto()
    print("\nTodos los PDFs generados correctamente.")


if __name__ == "__main__":
    main()
