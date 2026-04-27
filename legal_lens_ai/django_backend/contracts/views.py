from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ContractUploadForm
from .models import Contract


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
            contract.status = Contract.Status.PENDING
            contract.save()
            # Semana 2-3: aqui se llamara a FastAPI para procesar el PDF
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
