from __future__ import annotations

from typing import Any

import requests
from django.conf import settings


class AIEngineError(RuntimeError):
    """Cualquier fallo hablando con el microservicio de IA."""


def health() -> dict[str, Any]:
    """Comprueba que el microservicio esta vivo. Devuelve el JSON del endpoint."""
    try:
        r = requests.get(f"{settings.FASTAPI_URL}/health", timeout=5)
        r.raise_for_status()
        return r.json()
    except requests.RequestException as exc:
        raise AIEngineError(f"ai-engine no responde: {exc}") from exc


def extract_pdf(pdf_bytes: bytes, filename: str = "contract.pdf", timeout: int = 60) -> dict[str, Any]:
    """
    Envia el PDF al microservicio y devuelve la respuesta JSON con el texto.
    """
    files = {"file": (filename, pdf_bytes, "application/pdf")}
    try:
        r = requests.post(f"{settings.FASTAPI_URL}/extract", files=files, timeout=timeout)
        r.raise_for_status()
        return r.json()
    except requests.RequestException as exc:
        raise AIEngineError(f"Error en /extract: {exc}") from exc


def audit_contract(
    pdf_bytes: bytes,
    contract_type: str,
    filename: str = "contract.pdf",
    timeout: int = 180,
) -> dict[str, Any]:
    """
    Pipeline completo: extraccion + auditoria con el agente Gemini.
    contract_type: 'RENTAL' o 'NDA'.
    """
    files = {"file": (filename, pdf_bytes, "application/pdf")}
    data = {"contract_type": contract_type.upper()}
    try:
        r = requests.post(
            f"{settings.FASTAPI_URL}/audit",
            files=files,
            data=data,
            timeout=timeout,
        )
        r.raise_for_status()
        return r.json()
    except requests.HTTPError as exc:
        detail = ""
        try:
            detail = exc.response.json().get("detail", "")
        except Exception:
            detail = exc.response.text if exc.response is not None else str(exc)
        raise AIEngineError(f"Error en /audit ({exc.response.status_code}): {detail}") from exc
    except requests.RequestException as exc:
        raise AIEngineError(f"Error en /audit: {exc}") from exc
