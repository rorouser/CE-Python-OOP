import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from . import ai_client
from .forms import ContractUploadForm
from .models import AuditReport, Contract

log = logging.getLogger(__name__)


@login_required
def dashboard(request):
    """Listado de contratos del abogado."""
    contracts = Contract.objects.filter(lawyer=request.user)
    stats = {
        "total": contracts.count(),
        "clean": contracts.filter(status=Contract.Status.CLEAN).count(),
        "flagged": contracts.filter(status=Contract.Status.FLAGGED).count(),
        "pending": contracts.filter(
            status__in=[Contract.Status.PENDING, Contract.Status.PROCESSING]
        ).count(),
    }
    return render(
        request,
        "contracts/dashboard.html",
        {"contracts": contracts, "stats": stats},
    )


@login_required
def upload(request):
    """Subida de un contrato."""
    if request.method == "POST":
        form = ContractUploadForm(request.POST, request.FILES)
        if form.is_valid():
            contract = form.save(commit=False)
            contract.lawyer = request.user
            contract.status = Contract.Status.PROCESSING
            contract.save()

            # --- Semana 3: extraccion + auditoria IA via microservicio FastAPI ---
            try:
                contract.pdf_file.open("rb")
                pdf_bytes = contract.pdf_file.read()
                contract.pdf_file.close()

                resp = ai_client.audit_contract(
                    pdf_bytes,
                    contract_type=contract.contract_type,
                    filename=contract.pdf_file.name,
                )
                audit = resp.get("audit", {})
                red_flags = audit.get("red_flags", []) or []
                is_clean = bool(audit.get("is_clean")) and not red_flags

                AuditReport.objects.update_or_create(
                    contract=contract,
                    defaults={
                        "extracted_text": resp.get("extracted_text", ""),
                        "key_data": audit.get("key_data", {}) or {},
                        "red_flags": red_flags,
                        "summary": audit.get("summary", "") or "",
                        "processing_time_ms": resp.get("total_time_ms", 0),
                    },
                )
                contract.status = (
                    Contract.Status.CLEAN if is_clean else Contract.Status.FLAGGED
                )
                contract.save(update_fields=["status"])
                if is_clean:
                    messages.success(request, "Contrato auditado: sin banderas rojas.")
                else:
                    messages.warning(
                        request,
                        f"Auditoria completada: {len(red_flags)} bandera(s) roja(s) detectada(s).",
                    )
            except ai_client.AIEngineError as exc:
                log.exception("Fallo al contactar con ai-engine")
                contract.status = Contract.Status.ERROR
                contract.save(update_fields=["status"])
                messages.error(request, f"No se pudo procesar el PDF: {exc}")

            return redirect("contracts:detail", pk=contract.pk)
    else:
        form = ContractUploadForm()
    return render(request, "contracts/upload.html", {"form": form})


@login_required
def detail(request, pk):
    """Detalle de un contrato (su informe de auditoria)."""
    contract = get_object_or_404(Contract, pk=pk)
    if contract.lawyer != request.user and not request.user.is_staff:
        return HttpResponseForbidden("No tienes permiso para ver este contrato.")
    report = getattr(contract, "report", None)
    return render(
        request,
        "contracts/detail.html",
        {"contract": contract, "report": report},
    )
