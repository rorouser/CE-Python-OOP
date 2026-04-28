"""
LegalLens AI - Microservicio de IA (FastAPI).

Semana 2: extraccion de texto de PDFs (PyMuPDF + fallback pdfplumber).
Semana 3: anadira el agente de auditoria con Gemini sobre el texto extraido.
"""
from __future__ import annotations

import io
import logging
import time
from typing import Literal

import fitz  # PyMuPDF
import pdfplumber
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field

from agent.auditor import audit as run_audit
from contracts import AuditResult, get_contract

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("legallens.ai")

app = FastAPI(
    title="LegalLens AI Engine",
    description="Microservicio interno de extraccion y analisis de contratos.",
    version="0.2.0",
)


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------
class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"
    service: str = "legallens-ai"
    version: str = "0.2.0"


class PageText(BaseModel):
    page: int
    text: str
    char_count: int


class ExtractResponse(BaseModel):
    filename: str
    num_pages: int
    total_chars: int
    extractor: Literal["pymupdf", "pdfplumber"]
    processing_time_ms: int
    pages: list[PageText] = Field(default_factory=list)
    full_text: str


# ---------------------------------------------------------------------------
# Extractores
# ---------------------------------------------------------------------------
def _extract_pymupdf(pdf_bytes: bytes) -> tuple[list[str], int]:
    pages: list[str] = []
    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        for page in doc:
            pages.append(page.get_text("text") or "")
        return pages, doc.page_count


def _extract_pdfplumber(pdf_bytes: bytes) -> tuple[list[str], int]:
    pages: list[str] = []
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            pages.append(page.extract_text() or "")
        return pages, len(pdf.pages)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.get("/health", response_model=HealthResponse, tags=["meta"])
def health() -> HealthResponse:
    return HealthResponse()


@app.get("/", tags=["meta"])
def root() -> dict[str, str]:
    return {
        "service": "LegalLens AI Engine",
        "docs": "/docs",
        "health": "/health",
    }


@app.post("/extract", response_model=ExtractResponse, tags=["pdf"])
async def extract_pdf(file: UploadFile = File(...)) -> ExtractResponse:
    """
    Recibe un PDF y devuelve su texto pagina a pagina.
    Usa PyMuPDF por defecto; si falla o no extrae nada, intenta pdfplumber.
    """
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Solo se aceptan archivos .pdf")

    pdf_bytes = await file.read()
    if not pdf_bytes:
        raise HTTPException(status_code=400, detail="El archivo esta vacio")

    log.info("Extrayendo PDF: %s (%d bytes)", file.filename, len(pdf_bytes))
    started = time.perf_counter()

    extractor: Literal["pymupdf", "pdfplumber"] = "pymupdf"
    try:
        pages_text, num_pages = _extract_pymupdf(pdf_bytes)
        # Si PyMuPDF devuelve todo vacio (PDF escaneado/mal formado), probamos pdfplumber
        if not any(p.strip() for p in pages_text):
            log.warning("PyMuPDF no extrajo texto, fallback a pdfplumber")
            pages_text, num_pages = _extract_pdfplumber(pdf_bytes)
            extractor = "pdfplumber"
    except Exception as exc:
        log.exception("Fallo PyMuPDF, intentando pdfplumber")
        try:
            pages_text, num_pages = _extract_pdfplumber(pdf_bytes)
            extractor = "pdfplumber"
        except Exception as inner:
            raise HTTPException(
                status_code=422,
                detail=f"No se pudo procesar el PDF: {exc} / {inner}",
            ) from inner

    elapsed_ms = int((time.perf_counter() - started) * 1000)
    pages = [
        PageText(page=i + 1, text=t, char_count=len(t))
        for i, t in enumerate(pages_text)
    ]
    full_text = "\n\n".join(pages_text).strip()

    return ExtractResponse(
        filename=file.filename,
        num_pages=num_pages,
        total_chars=len(full_text),
        extractor=extractor,
        processing_time_ms=elapsed_ms,
        pages=pages,
        full_text=full_text,
    )


# ---------------------------------------------------------------------------
# /audit - Semana 3
# ---------------------------------------------------------------------------
class AuditResponse(BaseModel):
    filename: str
    contract_type: str
    extractor: Literal["pymupdf", "pdfplumber"]
    extract_time_ms: int
    audit_time_ms: int
    total_time_ms: int
    extracted_text: str
    audit: AuditResult


@app.post("/audit", response_model=AuditResponse, tags=["audit"])
async def audit_contract(
    file: UploadFile = File(..., description="PDF del contrato"),
    contract_type: str = Form(..., description="RENTAL o NDA"),
) -> AuditResponse:
    """
    Pipeline completo: PDF -> texto -> agente IA -> AuditResult estructurado.
    """
    # 1) Validacion + extraccion (reutiliza el endpoint /extract internamente)
    extracted = await extract_pdf(file)

    if extracted.total_chars < 50:
        raise HTTPException(
            status_code=422,
            detail="El PDF no contiene texto suficiente para auditarlo "
                   "(posiblemente escaneado).",
        )

    # 2) Selecciona la subclase correcta y lanza el agente
    try:
        contract_obj = get_contract(contract_type, extracted.full_text)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    try:
        audit_result, audit_ms = run_audit(contract_obj)
    except RuntimeError as exc:  # GOOGLE_API_KEY no configurada
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        log.exception("Fallo al ejecutar el agente")
        raise HTTPException(status_code=500, detail=f"Error en el agente IA: {exc}") from exc

    return AuditResponse(
        filename=extracted.filename,
        contract_type=contract_type.upper(),
        extractor=extracted.extractor,
        extract_time_ms=extracted.processing_time_ms,
        audit_time_ms=audit_ms,
        total_time_ms=extracted.processing_time_ms + audit_ms,
        extracted_text=extracted.full_text,
        audit=audit_result,
    )
