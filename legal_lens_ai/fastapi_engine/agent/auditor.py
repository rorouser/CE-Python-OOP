"""
Agente auditor de contratos basado en Gemini (LangChain + structured output).

Recibe un BaseContract (con su texto y metadatos) y devuelve un AuditResult
estructurado: datos clave, banderas rojas y resumen.
"""
from __future__ import annotations

import logging
import os
import time

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from contracts import AuditResult, BaseContract

log = logging.getLogger("legallens.agent")

# Mismo modelo que ya validaste con cuota libre en los ejercicios de AI Engineering.
MODEL_NAME = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash-lite")


def _build_llm() -> ChatGoogleGenerativeAI:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key or api_key == "tu_api_key_aqui":
        raise RuntimeError(
            "GOOGLE_API_KEY no configurada. Anade tu key en legal_lens_ai/.env."
        )
    return ChatGoogleGenerativeAI(
        model=MODEL_NAME,
        temperature=0.1,         # auditoria legal: queremos respuestas estables
        google_api_key=api_key,
    )


def audit(contract: BaseContract) -> tuple[AuditResult, int]:
    """
    Audita el contrato y devuelve (resultado, tiempo_ms).
    Usa structured output: el LLM rellena directamente el schema AuditResult.
    """
    llm = _build_llm().with_structured_output(AuditResult)

    prompt = ChatPromptTemplate.from_messages([
        ("system", contract.build_audit_prompt()),
        ("human",
         "=== CONTRATO A AUDITAR ===\n"
         "Tipo declarado: {contract_type}\n\n"
         "{text}\n\n"
         "Devuelve el AuditResult con contract_type=\"{contract_type}\".")
    ])

    chain = prompt | llm
    started = time.perf_counter()
    log.info("Auditando contrato tipo=%s chars=%d", contract.display_name, len(contract.text))
    result: AuditResult = chain.invoke({
        "contract_type": contract.display_name,
        "text": contract.text,
    })
    elapsed_ms = int((time.perf_counter() - started) * 1000)

    # Coherencia: si hay banderas rojas, no esta limpio
    if result.red_flags and result.is_clean:
        result.is_clean = False

    log.info(
        "Auditoria completada: red_flags=%d is_clean=%s tiempo=%dms",
        len(result.red_flags), result.is_clean, elapsed_ms,
    )
    return result, elapsed_ms
