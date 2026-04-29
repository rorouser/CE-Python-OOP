"""
Comando de prueba: verifica la comunicacion Django -> FastAPI por la red interna.

Uso:
    python manage.py test_ai_engine                         # solo /health
    python manage.py test_ai_engine --pdf /ruta/al/file.pdf # extrae un PDF
"""
from __future__ import annotations

from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from contracts import ai_client


class Command(BaseCommand):
    help = "Smoke test del microservicio FastAPI (ai-engine)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--pdf",
            type=str,
            default=None,
            help="Ruta a un PDF dentro del contenedor para enviarlo a /extract",
        )
        parser.add_argument(
            "--audit",
            type=str,
            choices=["RENTAL", "NDA"],
            default=None,
            help="Si se indica, llama tambien a /audit con ese tipo de contrato",
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("[1/2] GET /health ..."))
        try:
            data = ai_client.health()
        except ai_client.AIEngineError as exc:
            raise CommandError(str(exc)) from exc
        self.stdout.write(self.style.SUCCESS(f"  OK -> {data}"))

        pdf_path = options.get("pdf")
        if not pdf_path:
            self.stdout.write("Sin --pdf, fin.")
            return

        path = Path(pdf_path)
        if not path.is_file():
            raise CommandError(f"No existe el fichero: {pdf_path}")

        self.stdout.write(self.style.NOTICE(f"[2/2] POST /extract con {path.name} ..."))
        try:
            resp = ai_client.extract_pdf(path.read_bytes(), filename=path.name)
        except ai_client.AIEngineError as exc:
            raise CommandError(str(exc)) from exc

        self.stdout.write(self.style.SUCCESS(
            f"  OK -> paginas={resp['num_pages']} chars={resp['total_chars']} "
            f"extractor={resp['extractor']} tiempo={resp['processing_time_ms']}ms"
        ))
        preview = resp["full_text"][:300].replace("\n", " ")
        self.stdout.write(f"  Preview: {preview}...")

        contract_type = options.get("audit")
        if not contract_type:
            return

        self.stdout.write(self.style.NOTICE(
            f"[3/3] POST /audit con tipo {contract_type} ..."
        ))
        try:
            audit_resp = ai_client.audit_contract(
                path.read_bytes(), contract_type=contract_type, filename=path.name
            )
        except ai_client.AIEngineError as exc:
            raise CommandError(str(exc)) from exc

        a = audit_resp["audit"]
        rf = a.get("red_flags", [])
        self.stdout.write(self.style.SUCCESS(
            f"  OK -> is_clean={a['is_clean']} red_flags={len(rf)} "
            f"extract_ms={audit_resp['extract_time_ms']} "
            f"audit_ms={audit_resp['audit_time_ms']}"
        ))
        self.stdout.write(f"  Resumen: {a.get('summary', '')}")
        for i, flag in enumerate(rf, 1):
            self.stdout.write(
                f"   [{i}] [{flag.get('severidad', '?')}] "
                f"{flag.get('clausula', '')} -> {flag.get('problema', '')} "
                f"({flag.get('articulo_legal', '')})"
            )
