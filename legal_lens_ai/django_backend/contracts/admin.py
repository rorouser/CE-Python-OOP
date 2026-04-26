from django.contrib import admin

from .models import AuditReport, Contract


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "client_name",
        "contract_type",
        "lawyer",
        "status",
        "uploaded_at",
    )
    list_filter = ("contract_type", "status", "uploaded_at")
    search_fields = ("client_name", "lawyer__username", "lawyer__email")
    date_hierarchy = "uploaded_at"
    readonly_fields = ("uploaded_at",)


@admin.register(AuditReport)
class AuditReportAdmin(admin.ModelAdmin):
    list_display = ("id", "contract", "num_red_flags", "processing_time_ms", "created_at")
    list_filter = ("created_at",)
    readonly_fields = ("created_at", "processing_time_ms")
    search_fields = ("contract__client_name",)
